### API Resources
  - [GET /boundaries](#get-boundaries_datasets)
  - [POST /boundaries](#post-boundaries_dataset)
  - [GET /boundaries/[boundary_id]](#get-boundaries_dataset)

### GET /boundaries

Returns all BoundaryDatasets stored

Example: GET  http://example.com/boundaries

Response body:

    [
      {
          "boundary_data_set": [
              {
                  "boundary": "RO23$))))P12$)))34$))))S56$)))))",
                  "data": "test"
              },
              {
                  "boundary": "RP10$))1$)))2$))))",
                  "data": "test"
              },
              {
                  "boundary": "RR1$))2$))))",
                  "data": "test"
              }
          ]
      },
      {
          "boundary_data_set": [
              {
                  "boundary": "RQ1$))2$))))",
                  "data": "test"
              },
              {
                  "boundary": "RQ3$))4$))))",
                  "data": "test"
              }
          ]
      }
    ]

### POST /boundaries

Insert a BoundaryDataset

Example: POST  http://example.com/boundaries

Request body:

    {
          "boundary_data_set": [
              {
                  "boundary": "P1P2P3",
                  "data": "test"
              },
              {
                  "boundary": "Q14Q15",
                  "data": "test"
              },
              {
                  "boundary": "O22O23",
                  "data": "test"
              }
          ]
     }



### GET /boundaries/[id]

Returns all BoundaryDatasets containing the boundary with that id

Example: GET  http://example.com/boundaries/P10P11P2

Response body:

    [
      {
          "boundary_data_set": [
              {
                  "boundary": "RO23$))))P12$)))34$))))S56$)))))",
                  "data": "test"
              },
              {
                  "boundary": "RP10$))1$)))2$))))",
                  "data": "test"
              },
              {
                  "boundary": "RR1$))2$))))",
                  "data": "test"
              }
          ]
      }
    ]



