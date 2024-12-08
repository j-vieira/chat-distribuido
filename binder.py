from xmlrpc.server import SimpleXMLRPCServer

registered_procedures = {}

def register_procedure(name, port, address='localhost'):
    if name in registered_procedures:
        print(f"Procedure '{name}' já registrada na porta {registered_procedures[name]}.")
        return f"Procedure '{name}' já registrada na porta {registered_procedures[name]}."
    
    registered_procedures[name] = (address, port)
    print(f"Procedure '{name}' registrada no endereço {address}:{port}.")
    return f"Procedure '{name}' registrada com sucesso no endereço {address}:{port}."

def lookup_procedure(name):
    if name in registered_procedures:
        return registered_procedures[name]
    else:
        return f"Procedure '{name}' não encontrada."

binderServer = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
    
print("Binder aguardando novos registros...")

binderServer.register_function(register_procedure, "register_procedure")
binderServer.register_function(lookup_procedure, "lookup_procedure")

binderServer.serve_forever()
