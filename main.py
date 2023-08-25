# import time
# from typing import Optional, Union
# from fastapi.responses import HTMLResponse
# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from fastapi import WebSocket

# # app = FastAPI()

# # class Middleware(BaseHTTPMiddleware):
# #     print("ss")
# #     async def dispatch(self, request: Request, call_next):
# #         print("ssss")
# #         start_time = time.time()
# #         print(start_time)
# #         response = await call_next(request)
# #         process_time = time.time() - start_time
# #         response.headers["X-Process-Time"] = str(process_time)
# #         return response
    
# # app.add_middleware(Middleware)

# from fastapi import (
#     Cookie,
#     Depends,
#     FastAPI,
#     Query,
#     WebSocket,
#     WebSocketException,
#     status,
# )
# from fastapi.responses import HTMLResponse
# from typing_extensions import Annotated

# app = FastAPI()

# # html = """
# # <!DOCTYPE html>
# # <html>
# #     <head>
# #         <title>Chat</title>
# #     </head>
# #     <body>
# #         <h1>WebSocket Chat</h1>
# #         <form action="" onsubmit="sendMessage(event)">
# #             <input type="text" id="messageText" autocomplete="off"/>
# #             <button>Send</button>
# #         </form>
# #         <ul id='messages'>
# #         </ul>
# #         <script>
# #             var ws = new WebSocket("ws://localhost:8000/ws");
# #             ws.onmessage = function(event) {
# #                 var messages = document.getElementById('messages')
# #                 var message = document.createElement('li')
# #                 var content = document.createTextNode(event.data)
# #                 message.appendChild(content)
# #                 messages.appendChild(message)
# #             };
# #             function sendMessage(event) {
# #                 var input = document.getElementById("messageText")
# #                 ws.send(input.value)
# #                 input.value = ''
# #                 event.preventDefault()
# #             }
# #         </script>
# #     </body>
# # </html>
# # """


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
#             <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
#             <button onclick="connect(event)">Connect</button>
#             <hr>
#             <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#         var ws = null;
#             function connect(event) {
#                 var itemId = document.getElementById("itemId")
#                 var token = document.getElementById("token")
#                 ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
#                 ws.onmessage = function(event) {
#                     var messages = document.getElementById('messages')
#                     var message = document.createElement('li')
#                     var content = document.createTextNode(event.data)
#                     message.appendChild(content)
#                     messages.appendChild(message)
#                 };
#                 event.preventDefault()
#             }
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

# @app.get("/")
# async def get():
#     return HTMLResponse(html)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


# # async def get_cookie_or_token(
# #     websocket: WebSocket,
# #     session: Annotated[Union[str, None], Cookie()] = None,
# #     token: Annotated[Union[str, None], Query()] = None,
# # ):
# #     if session is None and token is None:
# #         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
# #     return session or token


# # @app.websocket("/items/{item_id}/ws")
# # async def websocket_endpoint(
# #     *,
# #     websocket: WebSocket,
# #     item_id: str,
# #     q: Union[int, None] = None,
# #     cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
# # ):
# #     await websocket.accept()
# #     while True:
# #         data = await websocket.receive_text()
# #         await websocket.send_text(
# #             f"Session cookie or query token value is: {cookie_or_token}"
# #         )
# #         if q is not None:
# #             await websocket.send_text(f"Query parameter q is: {q}")
# #         await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")


# # @app.get("/")
# # def read_root():
# #     return {"Hello": "World"}

# @app.get('/blog')
# def test(limit: int, published: Optional[bool]= False):
#     if published:
#         print(published,"pub")
#         return {"check": f'{limit} is the key'}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



# class Blog(BaseModel):
#     title: str
#     name: str
#     published: Optional[bool] 

# @app.post("/postest")
# def postest(blog: Blog):
#     return {"data": f'blog is created with title as {blog.title} and name {blog.name}'}