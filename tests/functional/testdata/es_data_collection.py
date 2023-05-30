test_data = {
    'genres': [
        {'uuid': '3b555e24-bd6f-4566-a98a-e9cfd1ecae0d', 'name': 'Action'},
        {'uuid': '0402143a-19a9-495d-9cca-e65e9e5e4509', 'name': 'Adventure'},
        {'uuid': 'b879e9ee-27a7-48d5-bf98-98878e4f0371', 'name': 'Biography'},
        {'uuid': 'e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a', 'name': 'Drama'},
        {'uuid': '5b73b2c3-dac0-4c48-b917-a8efba4b3456', 'name': 'Multiplication'}
    ],

    'persons': [
        {'uuid': '26dcf837-0327-4777-81f0-f0a59109769c', 'full_name': 'Ivan Ivanov',
         'films': [{'uuid': '54dceed7-2ce8-4657-8a24-ab7a40bb1db3', 'roles': ['actor']},
                   {'uuid': '70a6ed85-6fa1-4ec7-a6bb-5b1f2670c0a3', 'roles': ['actor']},
                   ]},
        {'uuid': '2cd05c17-3956-4ceb-8d75-a88a2a0ad34b', 'full_name': 'Masha Petrova',
         'films': [{'uuid': 'd3fd996d-e843-4d71-991c-0e66649987b0', 'roles': ['actor']},
                   {'uuid': 'ce8432ee-adba-49a7-8ae2-993d43730860', 'roles': ['director']}]},
        {'uuid': 'c177c3d5-b562-410d-931c-702f69fbb638', 'full_name': 'Sergey Tretyakov',
         'films': [{'uuid': '16364492-5136-4fe4-b230-9906b8b06e77', 'roles': ['director']},
                   {'uuid': 'bfca293c-b916-4fdf-908e-c36045e61e88', 'roles': ['actor', 'director']},
                   {'uuid': 'ff8f1890-d8f2-4400-9372-d699c60ff2ac', 'roles': ['actor']}]},
        {'uuid': 'eae29d9d-5248-45fa-9cfd-fa9a03e8d0f2', 'full_name': 'Irina Korobko',
         'films': [{'uuid': 'bfca293c-b916-4fdf-908e-c36045e61e88', 'roles': ['writer']}]},
        {'uuid': 'ec64d43b-806d-42b6-99c9-9c4b89cdcebf', 'full_name': 'Evgeniy Myshkin',
         'films': []}
    ],
    'films': [{"uuid": "b34e2bcf-2591-4cf8-a921-28b9f276b14c", "imdb_rating": 8.4,
               "genre": [{"uuid": "e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a", "name": "Drama"},
                         {"uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Sci-Fi"},
                         {"uuid": "327f8e0e-5ba1-4d53-b30a-1ebf5b685e5c", "name": "Thriller"}
                         ],
               "title": "USS Callister",
               "description": "A brilliant but socially awkward programmer creates a virtual reality "
                              "world that allows him to live out his dream of being a captain of a spaceship. "
                              "However, his power-hungry tendencies lead him to abuse his digital crew members.",
               "director": ["Toby Haynes"],
               "actors_names": ["Jesse Plemons", "Cristin Milioti", "Jimmi Simpson"],
               "writers_names": ["Charlie Brooker", "William Bridges"],
               "actors": [{"uuid": "aa3d3a7b-6f85-4f37-b6e4-17d0025b775e", "name": "Jesse Plemons"},
                          {"uuid": "7d50c6ec-c0f6-40fa-9027-8c1fc07a4176",
                           "name": "Cristin Milioti"},
                          {"uuid": "0b8b0516-3a97-4af9-9a03-dc63de6483cb",
                           "name": "Jimmi Simpson"}],
               "writers": [
                   {"uuid": "2576c9a7-91eb-4141-a6e3-d3b3c031f37a", "name": "Charlie Brooker"},
                   {"uuid": "ed31f7c5-8826-4a57-9a90-7b2b1c77a390", "name": "William Bridges"}]},
              {"uuid": "82d1c9cf-7ca5-45f7-b7eb-aa662d8a7f48", "imdb_rating": 8.0,
               "genre": [{"uuid": "e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a", "name": "Drama"},
                         {"uuid": "3e3c9f7d-475d-48e3-b2c6-bd532456e546", "name": "Sci-Fi"},
                         {"uuid": "0ef09867-1726-4b67-a166-52daae48fc6f", "name": "Thriller"}],
               "title": "Nosedive",
               "description": "In a world where people can rate each other out of five stars for every "
                              "interaction they have, a woman sets out to raise her score in order to "
                              "secure a coveted apartment and a better life.",
               "director": ["Joe Wright"],
               "actors_names": ["Bryce Dallas Howard", "Alice Eve", "Cherry Jones"],
               "writers_names": ["Charlie Brooker", "Michael Schur", "Rashida Jones"],
               "actors": [
                   {"uuid": "360b86da-f48b-418c-b6c9-7dcefacd28c3", "name": "Bryce Dallas Howard"},
                   {"uuid": "f97f9b4a-fbe4-4e52-a7a6-45b0a8333c3f", "name": "Alice Eve"},
                   {"uuid": "75247d11-78d3-442e-8b25-2dc7c0e29d13", "name": "Cherry Jones"}],
               "writers": [
                   {"uuid": "2576c9a7-91eb-4141-a6e3-d3b3c031f37a", "name": "Charlie Brooker"},
                   {"uuid": "83e97338-0a0a-48fc-8d06-6f826c6fcb78", "name": "Michael Schur"},
                   {"uuid": "5c83541f-16c5-470f-a364-041bfbe67e19", "name": "Rashida Jones"}]},
              {"uuid": "7bdfaf70-2f7a-4392-9986-c8e6aa88d6e4", "imdb_rating": 7.3,
               "genre": [{"uuid": "41cc3dcb-d5de-46eb-9e62-2eb23d8aaf41", "name": "Comedy"},
                         {"uuid": "e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a", "name": "Drama"}],
               "title": "Terminal",
               "description": "An Eastern European tourist becomes stranded in JFK airport after her passport "
                              "is stolen. She befriends a group of airport workers, including an American "
                              "janitor and a customs officer, and tries to make the best of her situation while "
                              "awaiting resolution of her legal status.",
               "director": ["Steven Spielberg"],
               "actors_names": ["Tom Hanks", "Catherine Zeta-Jones", "Stanley Tucci"],
               "writers_names": ["Sacha Gervasi"],
               "actors": [{"uuid": "f8b18c68-c2f9-439c-ae84-319a84bca7fc", "name": "Tom Hanks"},
                          {"uuid": "7ce4f4bb-6787-418d-b6c4-b26737efb6c1",
                           "name": "Catherine Zeta-Jones"},
                          {"uuid": "a8c48d7b-69f1-44c9-9f05-7b20b981139d",
                           "name": "Stanley Tucci"}],
               "writers": [
                   {"uuid": "29f8dbf5-7e61-4682-8197-5c2f3d5f2911", "name": "Sacha Gervasi"}]},
              {"uuid": "70a6ed85-6fa1-4ec7-a6bb-5b1f2670c0a3", "imdb_rating": 7.6,
               "genre": [{"uuid": "0402143a-19a9-495d-9cca-e65e9e5e4509", "name": "Adventure"},
                         {"uuid": "1a3fb3b6-d2f6-4a75-bf5d-e0405e5d40f8", "name": "Family"},
                         {"uuid": "d906c8e9-f9ea-497c-b555-3297c4a158b4", "name": "Fantasy"}],
               "title": "Harry Potter and the Half-Blood Prince",
               "description": "As Harry Potter begins his sixth year at Hogwarts, he discovers a mysterious "
                              "textbook marked as the property of the Half-Blood Prince and "
                              "begins to unravel the secrets of the past, including those of Voldemort "
                              "and his Death Eaters.",
               "director": ["David Yates"],
               "actors_names": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint", "Ivan Ivanov"],
               "writers_names": ["Steve Kloves", "J.K. Rowling"],
               "actors": [
                   {"uuid": "d84668de-7d95-43d6-aa97-60a5a6144435", "name": "Daniel Radcliffe"},
                   {"uuid": "bf41cdd7-2052-47fb-8e92-153b60a7f0a2", "name": "Emma Watson"},
                   {"uuid": "d3f518fb-8b3d-4d25-8b4e-f06f4b4e0b26", "name": "Rupert Grint"},
                   {"uuid": "26dcf837-0327-4777-81f0-f0a59109769c", "name": "Ivan Ivanov"}],
               "writers": [{"uuid": "343f7f92-068d-4a56-bcd5-5d5de5e1040c", "name": "Steve Kloves"},
                           {"uuid": "530d7b94-0a6a-4200-b70c-26212e6fa64d",
                            "name": "J.K. Rowling"}]},
              {"uuid": "8f26a39b-9a9f-4b1a-b8d7-139d1f5b5a91", "imdb_rating": 8.1,
               "genre": [{"uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Drama"},
                         {"uuid": "4fd4eb2c-b071-4c00-86c4-3071fd7a61c6", "name": "History"},
                         {"uuid": "860b3ee3-b3aa-4a67-885d-55d5966f0662", "name": "Romance"}],
               "title": "Gone with the Wind",
               "description": "A manipulative Southern belle carries on a turbulent affair with a blockade "
                              "runner during the American Civil War and Reconstruction periods.",
               "director": ["Victor Fleming"],
               "actors_names": ["Vivien Leigh", "Clark Gable", "Thomas Mitchell"],
               "writers_names": ["Margaret Mitchell", "Sidney Howard"],
               "actors": [{"uuid": "7a2c2b1d-1d81-4973-a3a3-3e3d91ed3449", "name": "Vivien Leigh"},
                          {"uuid": "d3811d7e-105a-49f7-a34a-786a579ea615", "name": "Clark Gable"},
                          {"uuid": "8f15d0c6-d4d6-4da4-8e6d-92edc9335c43",
                           "name": "Thomas Mitchell"}],
               "writers": [
                   {"uuid": "5d5b3d5b-3eaa-4b6d-9106-8a79af4c2f19", "name": "Margaret Mitchell"},
                   {"uuid": "15e44f83-5f2a-4c92-90d7-6dc9255ec5b3", "name": "Sidney Howard"}]}
              ]
}
