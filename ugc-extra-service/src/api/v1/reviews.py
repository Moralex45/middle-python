from __future__ import annotations

import uuid

import fastapi

import src.core.exceptions.repositories as repositories_exception
import src.models.http.events.review as http_reviews_models
import src.models.http.events.user_to_review_like as http_user_to_review_like_models
from src.core.utils import verify_auth_tokens
from src.repositories.review import (AsyncMongoDBReviewRepository,
                                     get_review_repository)
from src.repositories.user_to_film_like import (
    AsyncMongoDBUserToFilmLikeRepository, get_user_to_film_like_repository)
from src.repositories.user_to_review_like import (
    AsyncMongoDBUserToReviewLikeRepository, get_user_to_review_like_repository)
from src.utils.review_like_event import review_like_event

router = fastapi.APIRouter(prefix='/api/v1/reviews')


@router.post('/',
             response_model=http_reviews_models.Review,
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Создание новой рецензии в системе',
             summary='Endpoint позволяет создать новую рецензию в системе',
             tags=['Рецензии'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def create_review(
        http_review: http_reviews_models.ReviewCreation,
        user_to_film_likes_repository: AsyncMongoDBUserToFilmLikeRepository = fastapi.Depends(
            get_user_to_film_like_repository,
        ),
        review_repository: AsyncMongoDBReviewRepository = fastapi.Depends(
            get_review_repository,
        ),
        user_to_review_likes_repository: AsyncMongoDBUserToReviewLikeRepository = fastapi.Depends(
            get_user_to_review_like_repository,
        ),
) -> http_reviews_models.Review:
    try:
        review = await review_repository.create_review(
            http_review.user_id, http_review.movie_id, http_review.text,
        )

    except repositories_exception.DataAlreadyExistsError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='Review already exist')

    review_average_mark = await user_to_review_likes_repository.get_average_review_mark(review.id)
    user_to_film_mark = await user_to_film_likes_repository.get_like(review.user_id, review.movie_id)

    http_review_dict = review.to_dict(False)
    http_review_dict['user_to_film_like'] = user_to_film_mark
    http_review_dict['average_review_mark'] = review_average_mark

    return http_reviews_models.Review(**http_review_dict)


@router.get('/',
            response_model=list[http_reviews_models.Review],  # type:ignore
            status_code=fastapi.status.HTTP_201_CREATED,
            description='Просмотр рецензий в системе',
            summary='Endpoint позволяет просмотреть рецензии в системе',
            tags=['Рецензии'],
            dependencies=[fastapi.Depends(verify_auth_tokens)])
async def get_reviews(
        user_id: uuid.UUID | None = None,
        movie_id: uuid.UUID | None = None,
        user_to_film_likes_repository: AsyncMongoDBUserToFilmLikeRepository = fastapi.Depends(
            get_user_to_film_like_repository,
        ),
        review_repository: AsyncMongoDBReviewRepository = fastapi.Depends(
            get_review_repository,
        ),
        user_to_review_likes_repository: AsyncMongoDBUserToReviewLikeRepository = fastapi.Depends(
            get_user_to_review_like_repository,
        ),
) -> list[http_reviews_models.Review]:
    if user_id is None and movie_id is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='Pass at least one filter parameter')
    if user_id is not None and movie_id is not None:
        review = await review_repository.get_review_by_user_id_and_movie_id(user_id, movie_id)
        if review is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='User review does not exist')

        review_average_mark = await user_to_review_likes_repository.get_average_review_mark(review.id)
        user_to_film_mark = await user_to_film_likes_repository.get_like(review.user_id, review.movie_id)

        http_review_dict = review.to_dict(False)
        http_review_dict['user_to_film_like'] = user_to_film_mark
        http_review_dict['average_review_mark'] = review_average_mark

        return [http_reviews_models.Review(**http_review_dict)]

    reviews = []

    if user_id is not None:
        reviews = await review_repository.get_reviews_by_user_id(user_id)

    elif movie_id is not None:
        reviews = await review_repository.get_reviews_by_movie_id(movie_id)

    http_reviews = []

    for review in reviews:
        review_average_mark = await user_to_review_likes_repository.get_average_review_mark(review.id)
        user_to_film_mark = await user_to_film_likes_repository.get_like(review.user_id, review.movie_id)

        http_review_dict = review.to_dict(False)
        http_review_dict['user_to_film_like'] = user_to_film_mark
        http_review_dict['average_review_mark'] = review_average_mark

        http_reviews.append(http_reviews_models.Review(**http_review_dict))

    return http_reviews


@router.post('/create_like',
             response_model=http_user_to_review_like_models.UserToReviewLike,
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Создание нового лайка рецензии в системе',
             summary='Endpoint позволяет создать новый лайк рецензии в системе',
             tags=['Рецензии'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def create_review_like(
        http_review_like: http_user_to_review_like_models.UserToReviewLikeCreation,
        user_to_review_likes_repository: AsyncMongoDBUserToReviewLikeRepository = fastapi.Depends(
            get_user_to_review_like_repository,
        ),
) -> http_user_to_review_like_models.UserToReviewLike:
    try:
        user_review_like = await user_to_review_likes_repository.create_like(
            http_review_like.user_id, http_review_like.review_id, http_review_like.mark,
        )
        await review_like_event(review_id=http_review_like.review_id)
        return http_user_to_review_like_models.UserToReviewLike(**user_review_like.to_dict(False))

    except repositories_exception.DataAlreadyExistsError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='User review like already exist',
        )


@router.post('/delete_like',
             status_code=fastapi.status.HTTP_200_OK,
             description='Удаление лайка рецензии в системе',
             summary='Endpoint позволяет удалить лайк рецензии в системе',
             tags=['Рецензии'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def delete_review_like(
        review_id: uuid.UUID,
        user_id: uuid.UUID,
        user_to_review_likes_repository: AsyncMongoDBUserToReviewLikeRepository = fastapi.Depends(
            get_user_to_review_like_repository,
        ),
) -> None:
    try:
        await user_to_review_likes_repository.delete_like(user_id, review_id)

    except repositories_exception.DataDoesNotExistError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='User review like does not exist',
        )
