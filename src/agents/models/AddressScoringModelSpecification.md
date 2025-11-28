Create a class named LocationScoringModel in the models folder 
that implements the following specification:
It has the following properties:
request is an object property that has the following properties:
- address: string
- city: string
- state_province: string
- postal_code: string
- country: string
score: number
superfund_sites: array of objects, each object has the following properties:
- address: string
- city: string
- state_province: string
- postal_code: string
- country: string
- pollution_class:string
- pollution_type:string
- remediation_status
- remediation_start: date
- remediation_finish: date
- distance_miles: number

