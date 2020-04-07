### API Resources
  - [GET /bdatasets](#get-boundaries_datasets)
  - [POST /bdatasets](#post-boundaries_dataset)
  - [GET /bdatasets/[boundary_id]](#get-boundaries_dataset)
  - [GET /boundaries](#get-boundaries)
  - [GET /boundaries/[boundary_id]](#get-boundaries)
  - [DELETE /boundaries/[boundary_id]](#delete-boundaries)

### GET /bdatasets

Returns all BoundaryDatasets stored

Example: GET  http://example.com/bdatasets

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

### POST /bdatasets

Insert a BoundaryDataset

Example: POST  http://example.com/bdatasets

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



### GET /bdatasets/[boundary_id]

Returns all BoundaryDatasets containing the Boundary with that id

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  boundary_id | Path  | Boundary identifier (Cell identifier sequence)

Example: GET  http://example.com/bdatasets/P10P11P2

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

### GET /boundaries

Returns all Boundaries along with the Data associated to them.

#### Possible parameters

Parameters referring to the vertices of a polygon can be added 
to filter out those Boundaries that intersect it.

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  dlx | QueryParam  | x coordinate of lower left vertex of the polygon to intersect
|  dly | QueryParam  | y coordinate of lower left vertex of the polygon to intersect
|  urx | QueryParam  | x coordinate of upper right vertex of the polygon to intersect
|  ury | QueryParam  | y coordinate of upper right vertex of the polygon to intersect


| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  dlx | QueryParam  | x coordinate of lower left vertex of the polygon to intersect
|  dly | QueryParam  | y coordinate of lower left vertex of the polygon to intersect
|  drx | QueryParam  | x coordinate of lower right vertex of the polygon to intersect
|  dry | QueryParam  | y coordinate of lower right vertex of the polygon to intersect
|  urx | QueryParam  | x coordinate of upper right vertex of the polygon to intersect  
|  ury | QueryParam  | y coordinate of upper right vertex of the polygon to intersect
|  ulx | QueryParam  | x coordinate of upper left vertex of the polygon to intersect
|  uly | QueryParam  | y coordinate of upper left vertex of the polygon to intersect


Example: GET  http://example.com/boundaries

Response body:

    [
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
        },
        {
            "boundary": "RQ1$))2$))))",
            "data": "test"
        },
        {
            "boundary": "RQ3$))4$))))",
            "data": "test"
        }
    ]
    
Example: GET  http://example.com/boundaries/?dlx=-179.9999997096064&dly=12.895313217732834&urx=-90.00000014160271&ury=41.93785365811587

Response body:

    [
        {
            "boundary": "RO22$))3$)))))",
            "data": "test"
        }
    ]
    
### GET /boundaries/[boundary_id]

Returns the Boundary (or Boundaries if it exists in different BoundaryDatasets) 
with that id along with the Data associated to it.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  boundary_id | Path  | Boundary identifier (Cell identifier sequence)

Example: GET  http://example.com/boundaries/P1P2P3

Response body:

    [
        {
            "boundary": "RP1$))2$))3$))))",
            "data": "test"
        },
    ]


### DELETE /boundaries/[boundary_id]

Deletes the Boundary (or Boundaries if it exists in different BoundaryDatasets) 
with that id along with the Data associated to it.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  boundary_id | Path  | Boundary identifier (Cell identifier sequence)

Example: DELETE  http://example.com/boundaries/P1P2P3
