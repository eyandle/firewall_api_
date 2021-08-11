from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from DataModels import FirewallRequestModel
from FirewallSpreadsheet import FirewallSpreadsheet
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://127.0.0.1:3000',
    'http://127.0.0.1',
    'http://127.0.0.1:3000/'
    '*'
]
app = FastAPI()


@app.get("/firewall_request")
async def get_firewall_request():
    return {"message": "Hello World"}


@app.post("/firewall_request")
async def post_firewall_request(firewall_request: FirewallRequestModel):
    firewall = FirewallSpreadsheet()
    excel = firewall.parse_firewall_change(firewall_request)
    return StreamingResponse(excel,
                             headers={
                                 'Content-Disposition': f'attachment; filename="FWREQ-{firewall_request.ticket}.xlsx"',
                             },
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/firewall_request/last_spreadsheet")
async def post_firewall_request():
    excel = open('temp_fw_req.xlsx', 'rb')
    return StreamingResponse(excel,
                             headers={
                                 'Content-Disposition': f'attachment; filename="FWREQ-LAST-TICKET.xlsx"',
                             },
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
