# from fastapi import FastAPI, HTTPException
# import uvicorn
# from fastapi.utils import is_body_allowed_for_status_code
#
#
# from api.api_v1.endpoints.endpoint import organisation_route
# from pydantic import ValidationError
#
# # from api_clients.api_client_workers import WorkerServiceException
# from database.database_initialization import lifespain
#
# from http import HTTPStatus
#
# from fastapi import Response, status, Request
# from fastapi.responses import JSONResponse
#
#
# # async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
# #     headers = getattr(exc, "headers", None)
# #     if not is_body_allowed_for_status_code(exc.status_code):
# #         return Response(status_code=exc.status_code, headers=headers)
# #     payload = {'error': HTTPStatus(exc.status_code).name}
# #     if exc.detail:
# #         payload['message'] = exc.detail
# #         payload['LOL'] = 'Переопредлеление'
# #     return JSONResponse(status_code=exc.status_code, content=payload, headers=headers)
#
#
#
# # app = FastAPI(lifespan=lifespain, exception_handlers={HTTPException: http_exception_handler})
# app = FastAPI(lifespan=lifespain)
#
#
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     headers = getattr(exc, "headers", None)
#     payload = {'error': HTTPStatus(exc.status_code).name}
#     if exc.detail:
#         payload['message'] = exc.detail
#         payload['LOL'] = 'Модификатор'
#     return JSONResponse(status_code=exc.status_code, content=payload, headers=headers)
#
#
# # @app.exception_handler(ValidationError)
# # async def validation_exception_handler(request: Request, exc: ValidationError):
# #     headers = getattr(exc, "headers", None)
# #     payload = {}
# #     if exc.errors():
# #         payload['message'] = exc.errors()
# #         payload['LOL'] = 'Ошибка валидации'
# #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload, headers=headers)
# #
# #
# # @app.exception_handler(WorkerServiceException)
# # async def validation_exception_handler(request: Request, exc: WorkerServiceException):
# #     return JSONResponse(status_code=exc.status_code, content=dict({'message':exc.detail}))
#
# app.include_router(router=organisation_route, prefix='/api')
#
# if __name__ == "__main__":
#     uvicorn.run('main:app', reload=True)