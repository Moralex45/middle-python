import json
from tests.functional.settings import get_settings_instance

movies = [
   {
      "id": "6f871442-9c3d-47b0-8808-992ab97312d2",
      "imdb_rating": 7.6,
      "genre": [
         {
            "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
            "name": "Action"
         },
         {
            "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
            "name": "Sci-Fi"
         }
      ],
      "title": "Star Trek: Strategic Operations Simulator",
      "description": None,
      "directors_names": [

      ],
      "actors_names": [

      ],
      "writers_names": [

      ],
      "actors": [

      ],
      "writers": [

      ],
      "directors": [

      ]
   },
   {
      "id": "9905f1ff-5da7-4142-97e6-7a0677228493",
      "imdb_rating": 5.3,
      "genre": [
         {
            "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
            "name": "Western"
         },
         {
            "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
            "name": "Romance"
         }
      ],
      "title": "The Star Packer",
      "description": "John Travers and his Indian companion Yak are after the mysterious Shadow and his gang. \
                     When Sheriff Davis is killed, Travers becomes Sheriff. \
                     Catching two gang members, he learns of the room where the gang gets \
                     their orders from behind a fake wall safe and makes plans to trap the Shadow.",
      "directors_names": [
         "Robert N. Bradbury"
      ],
      "actors_names": [
         "George 'Gabby' Hayes",
         "Yakima Canutt",
         "John Wayne",
         "Verna Hillie"
      ],
      "writers_names": [
         "Robert N. Bradbury"
      ],
      "actors": [
         {
            "id": "0cf6a8b6-047a-4bab-a264-6fac8a630acb",
            "name": "George 'Gabby' Hayes"
         },
         {
            "id": "42e47d3b-e0a4-4ead-98fd-9e5f34633950",
            "name": "Yakima Canutt"
         },
         {
            "id": "ec92a961-92d7-473a-a33f-cfee63946c5a",
            "name": "John Wayne"
         },
         {
            "id": "fd338d5e-3f4c-454b-9480-b9bda18b6c55",
            "name": "Verna Hillie"
         }
      ],
      "writers": [
         {
            "id": "d575d52d-38e1-4a84-a40a-c7c34b965cd0",
            "name": "Robert N. Bradbury"
         }
      ],
      "directors": [
         {
            "id": "d575d52d-38e1-4a84-a40a-c7c34b965cd0",
            "name": "Robert N. Bradbury"
         }
      ]
   },
   {
      "id": "6f8dc3c8-2221-473f-81ff-0c25ad2c01a0",
      "imdb_rating": 5.9,
      "genre": [
         {
            "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
            "name": "Western"
         },
         {
            "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
            "name": "Romance"
         }
      ],
      "title": "The Broken Star",
      "description": "A deputy marshal is ordered to investigate the killing \
                     of a Mexican ranch hand by a fellow deputy, who claims self-defense. \
                     Using turn of the century forensic science and dogged determination, \
                     the deputy breaks down his partner's alibi and discovers that the \
                     lawman had killed the rancher for eight thousand dollars in gold \
                     that had been hidden in the Mexican's home. Now he must arrest \
                     his friend before the Mexican's gunslinging \
                     friends can kill him before he's tried for the crime.",
      "directors_names": [
         "Lesley Selander"
      ],
      "actors_names": [
         "Lita Baron",
         "Bill Williams",
         "Howard Duff",
         "Douglas Fowley"
      ],
      "writers_names": [
         "John C. Higgins"
      ],
      "actors": [
         {
            "id": "0be1188e-b4da-4e4f-8721-68eb909f29d8",
            "name": "Lita Baron"
         },
         {
            "id": "414644e0-8c89-47b6-b18f-7ce69cf5e8fd",
            "name": "Bill Williams"
         },
         {
            "id": "4ccbd2eb-17f1-4dca-bdaf-9d59edc4cfc1",
            "name": "Howard Duff"
         },
         {
            "id": "c4d1260c-ffe2-4763-a7a8-9d4909568db4",
            "name": "Douglas Fowley"
         }
      ],
      "writers": [
         {
            "id": "01ac4731-c027-453a-988a-78ce3a4e7554",
            "name": "John C. Higgins"
         }
      ],
      "directors": [
         {
            "id": "7aeb2f0e-40b2-4fab-9c3a-f8955f25c5aa",
            "name": "Lesley Selander"
         }
      ]
   }
]

genres = [
   {
      "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
      "name": "Action"
   },
   {
      "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
      "name": "Adventure"
   },
   {
      "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
      "name": "Sci-Fi"
   },
   {
      "id": "1cacff68-643e-4ddd-8f57-84b62538081a",
      "name": "Drama"
   }
]

persons = [
   {
      "id": "d7d930ac-2a74-4ab4-b76c-e373fcc4729e",
      "full_name": "James Cawley"
   },
   {
      "id": "0b3d9d9c-b5b8-413c-84b3-4319ec054299",
      "full_name": "Jeff Mailhotte"
   },
   {
      "id": "c408e242-dbfe-46ec-9ed3-84983fba17b1",
      "full_name": "Kimio Yabuki"
   },
   {
      "id": "788a9583-495d-46cd-8e8a-7cc1f28c786a",
      "full_name": "Eddie Allen"
   },
   {
      "id": "0cf6a8b6-047a-4bab-a264-6fac8a630acb",
      "full_name": "George 'Gabby' Hayes"
   }
]


def data_for_elastic():
    json_list = []
    for record in persons:
        index_info = {
            "index": {
               "_index": get_settings_instance().persons_elastic_search_index_name,
               "_id": record["id"]
            }
         }
        json_list.append(index_info)
        json_list.append(record)
    for record in movies:
        index_info = {
            "index": {
               "_index": get_settings_instance().movies_elastic_search_index_name,
               "_id": record["id"]
               }
            }
        json_list.append(index_info)
        json_list.append(record)
    for record in genres:
        index_info = {
            "index": {
               "_index": get_settings_instance().genres_elastic_search_index_name,
               "_id": record["id"]
               }
            }
        json_list.append(index_info)
        json_list.append(record)

    json_list = "\n".join(json.dumps(j) for j in json_list)
    json_list += "\n"
    return json_list
