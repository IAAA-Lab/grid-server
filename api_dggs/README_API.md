### API Resources
  - [GET /bdatasets](#get-boundaries_datasets)
  - [POST /bdatasets](#post-boundaries_dataset)
  - [GET /bdatasets/[bdatasets_id]](#get-boundaries_dataset)
  - [GET /bdatasets/[bdatasets_id]/[boundary_id]](#get-boundary-in-boundaries_dataset)  
  - [DELETE /bdatasets/[bdatasets_id]](#delete-boundaries_dataset)
  - [DELETE /bdatasets/[bdatasets_id]/[boundary_id]](#delete-boundary-in-boundaries_dataset)  
  - [GET /boundaries](#get-boundaries)
  - [GET /boundaries/[boundary_id]](#get-boundaries)
  - [DELETE /boundaries/[boundary_id]](#delete-boundaries)

### GET /bdatasets

Returns all BoundaryDatasets stored

Example: GET  http://example.com/bdatasets

Response body:

    [
      {
          "id": "id_1",
          "boundary_data_set": [
              {
                  "AUID": "RO23$))))P12$)))34$))))S56$)))))",
                  "boundary": "O23P12P34S56",
                  "data": "test"
              },
              {
                  "AUID": "RP10$))1$)))2$))))",
                  "boundary": "P10P11P2",
                  "data": "test"
              },
              {
                  "AUID": "RR1$))2$))))",
                  "boundary": "R1R2",
                  "data": "test"
              }
          ]
      },
      {
          "id": "id_2",
          "boundary_data_set": [
              {
                  "AUID": "RQ1$))2$))))",
                  "boundary": "Q1Q2",
                  "data": "test"
              },
              {
                  "AUID": "RQ3$))4$))))",
                  "boundary": "Q3Q4",
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
          "id": "id_1",
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



### GET /bdatasets/[bdatasets_id]

Returns the BoundaryDataset with that id.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  bdatasets_id | Path  | BoundaryDataset identifier

Example: GET  http://example.com/bdatasets/id_1

Response body:

    [
      {
          "id": "id_1",
          "boundary_data_set": [
              {
                  "AUID": "RO23$))))P12$)))34$))))S56$)))))",
                  "boundary": "O23P12P34S56",
                  "data": "test"
              },
              {
                  "AUID": "RP10$))1$)))2$))))",
                  "boundary": "P10P11P12",
                  "data": "test"
              },
              {
                  "AUID": "RR1$))2$))))",
                  "boundary": "R1R2",
                  "data": "test"
              }
          ]
      }
    ]


### GET /bdatasets/[bdatasets_id]/[boundary_id]

Returns the Boundary with that id along with the Data associated to it, in the BoundaryDataset
with that id.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  bdatasets_id | Path  | BoundaryDataset identifier
|  boundary_id | Path  | Boundary identifier (Cell identifier sequence)

Example: GET  http://example.com/bdatasets/id_1/P10P11P2

Response body:

    [
      {
          "id": "id_1",
          "boundary_data_set": [
              {
                  "AUID": "RP10$))1$)))2$))))",
                  "boundary": "P10P11P2",
                  "data": "test"
              },
          ]
      }
    ]

### DELETE /bdatasets/[bdatasets_id]

Deletes the BoundaryDataset with that id.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  bdatasets_id | Path  | BoundaryDataset identifier

Example: DELETE  http://example.com/bdatasets/id_1


### DELETE /bdatasets/[bdatasets_id]/[boundary_id]

Deletes the Boundary with that id along with the Data associated to it, in the BoundaryDataset
with that id.

#### Parameters

| Parameter | Parameter Type | Description |
| ------------- | ------------- | ------------- |
|  bdatasets_id | Path  | BoundaryDataset identifier
|  boundary_id | Path  | Boundary identifier (Cell identifier sequence)

Example: DELETE  http://example.com/bdatasets/id_1/P10P11P2


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
            "AUID": "RO23$))))P12$)))34$))))S56$)))))",
            "boundary": "O23P12P34S56",
            "data": "test"
        },
        {
            "AUID": "RP10$))1$)))2$))))",
            "boundary": "P10P11P2",
            "data": "test"
        },
        {
            "AUID": "RR1$))2$))))",
            "boundary": "R1R2",
            "data": "test"
        },
        {
            "AUID": "RQ1$))2$))))",
            "boundary": "Q1Q2",
            "data": "test"
        },
        {
            "AUID": "RQ3$))4$))))",
            "boundary": "Q3Q4",
            "data": "test"
        }
    ]
    
Example: GET  http://example.com/boundaries/?dlx=-179.9999997096064&dly=12.895313217732834&urx=-90.00000014160271&ury=41.93785365811587

Response body:

    [
        {
            "AUID": "RO22$))3$)))))",
            "boundary": "O22O23",
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
            "AUID": "RP1$))2$))3$))))",
            "boundary": "P1P2P3",
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
