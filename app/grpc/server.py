import grpc
from concurrent import futures


from app.grpc.generated import translation_pb2, translation_pb2_grpc
from app.services.translator import translation_service
from ..core.config import settings

class TranslatorServicer(translation_pb2_grpc.TranslatorServicer):
    def Translate(self, request, context):
        try:
            # Authorization via metadata (optional, double-check in Nest-level)
            md = dict(context.invocation_metadata())
            auth = md.get("authorization") or md.get(" Authorization")
            if not auth or not auth.startswith("Bearer "):
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing authorization")

            token = auth.split(" ", 1)[1]
            if token != settings.API_KEY:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        except Exception as e:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, str(e))

        try:
            translated = translation_service.translate(request.text)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Translation error: {e}")

        return translation_pb2.TranslateResponse(translated_text=translated)


# Start gRPC server with TLS + require client cert (mTLS)
def serve_grpc(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translation_pb2_grpc.add_TranslatorServicer_to_server(TranslatorServicer(), server )

    # Load TLS credentials
    #with open(TLS_KEY, "rb") as f: server_key = f.read()
    #with open(TLS_CERT, "rb") as f: server_cert = f.read()
    #with open(TLS_CA, "rb") as f: ca_cert = f.read()

    # Server credentials that require client certs
    # server_credentials = grpc.ssl_server_credentials( [(server_key, server_cert)], root_certificates=ca_cert, require_client_auth=True)
    # server.add_secure_port(f"{GRPC_HOST}:{GRPC_PORT}", server_credentials)
    # logger.info(f"gRPC server listening on {GRPC_HOST}:{GRPC_PORT} (TLS, mTLS enforced)")

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    return server


# Create secure channel with client cert
#channel = grpc.secure_channel(target, creds)
#stub = translate_pb2_grpc.TranslatorStub(channel)
#reqmsg = pb2.TranslateRequest(text=body.get("text",""), source=body.get("source",""), target=body.get("target",""))
#try:
#    resp = stub.Translate(reqmsg, metadata=(("authorization", key),), timeout=20)
#except grpc.RpcError as e:
#    raise HTTPException(status_code=500, detail=f"gRPC error: {e.code()} {e.details()}")
#return JSONResponse({"translated": resp.translated})


