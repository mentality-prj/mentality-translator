import grpc
from concurrent import futures

# Start gRPC server with TLS + require client cert (mTLS)
def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    translate_pb2_grpc.add_TranslatorServicer_to_server(TranslatorServicer(), server)

    # Load TLS credentials
    with open(TLS_KEY, "rb") as f: server_key = f.read()
    with open(TLS_CERT, "rb") as f: server_cert = f.read()
    with open(TLS_CA, "rb") as f: ca_cert = f.read()

    # Server credentials that require client certs
    server_credentials = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True
    )

    server.add_secure_port(f"{GRPC_HOST}:{GRPC_PORT}", server_credentials)
    logger.info(f"gRPC server listening on {GRPC_HOST}:{GRPC_PORT} (TLS, mTLS enforced)")
    server.start()
    return server

from grpc import ssl_channel_credentials
import proto.translate_pb2 as pb2

# Create secure channel with client cert
with open(TLS_KEY, "rb") as f: client_key = f.read()
with open(TLS_CERT, "rb") as f: client_cert = f.read()
with open(TLS_CA, "rb") as f: ca_cert = f.read()

creds = ssl_channel_credentials(root_certificates=ca_cert, private_key=client_key, certificate_chain=client_cert)
target = f"localhost:{GRPC_PORT}"
channel = grpc.secure_channel(target, creds)
stub = translate_pb2_grpc.TranslatorStub(channel)
reqmsg = pb2.TranslateRequest(text=body.get("text",""), source=body.get("source",""), target=body.get("target",""))
try:
    resp = stub.Translate(reqmsg, metadata=(("authorization", key),), timeout=20)
except grpc.RpcError as e:
    raise HTTPException(status_code=500, detail=f"gRPC error: {e.code()} {e.details()}")
return JSONResponse({"translated": resp.translated})


'''
from multiprocessing import context
from concurrent import futures
from transformers import pipeline
from proto import translate_pb2, translate_pb2_grpc

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn


from translate_pb2 import TranslateResponse
from translate_pb2_grpc import TranslatorServicer


# gRPC servicer
class TranslatorServicer(translate_pb2_grpc.TranslatorServicer):

    async def Translate(self, request, context):
        # Authorization via metadata (optional, double-check in Nest-level)
        md = dict(context.invocation_metadata())
        auth = md.get("authorization") or md.get(" Authorization")
        if not auth or not auth.startswith("Bearer "):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing authorization")

        token = auth.split(" ", 1)[1]
        if token != API_KEY:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        text = request.text
        target = request.target or "en"
        # Using pipeline synchronously
        try:
            out = translator_pipe(text, tgt_lang=target) if isinstance(translator_pipe, dict) else translator_pipe(text)
            # Many pipelines return list of dicts
            if isinstance(out, list):
                translated = out[0].get("translation_text") or out[0]
            elif isinstance(out, dict):
                translated = out.get("translation_text") or str(out)
            else:
                translated = str(out)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Translation error: {e}")

        return translate_pb2.TranslateResponse(translated=translated)


class TranslatorService(TranslatorServicer):
    async def Translate(self, request, context):
        text = request.text
        lang = request.target_lang

        # TODO: тут виклик моделі
        result = f"{text} -> translated to {lang}"

        return TranslateResponse(translated_text=result)




'''