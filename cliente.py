import threading, socket, argparse, os, sys
import tkinter as tk

class Envio(threading.Thread):

    #Recebe o input do usuario

    def __init__(self, sock, nome):

        super().__init__()
        self.sc = sock
        self.nome = nome
    
    def run(self):

        while True:

            print(f'{self.nome}: ', end='')
            sys.stdout.flush()
            mensagem = sys.stdin.readline()[:-1]
        
            #sair do chat
            if mensagem == 'QUIT':
                self.sc.sendall(f'{self.nome} saiu do chat'.encode('UTF-8'))
                break

            else:
                self.sc.sendall(f'{self.nome}: {mensagem}'.encode('UTF-8'))

        print('\nSaindo do chat...')
        self.sc.close()
        os._exit(0)


class Inbox(threading.Thread):

    def __init__(self, sock, nome):
        super().__init__()
        self.sc = sock
        self.nome = nome
        self.mensagens = tk.Listbox()

    def run(self):

        #recebe as mensagens do servidor e exibe
        while True:

            mensagem = self.sc.recv(1024).decode('UTF-8')
            
            try:
                if mensagem:
                    if self.mensagens:
                        self.mensagens.insert(tk.END, mensagem)
                        print('hi')
                        print(f'\r{mensagem}\n{self.nome}: ', end='')
                    
                    else:
                        print(f'\r{mensagem}\n{self.nome}: ', end='')
                
                else:
                    print('\nConexão perdida com o servidor :(')
                    print('\nSaindo...')
                    self.sc.close()
                    os._exit(0)
            except:
                print('\nConexão perdida com o servidor :(')
                print('\nSaindo...')
                self.sc.close()
                os._exit(0)


class Cliente:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome = None
        self.mensagens = tk.Listbox()

    def start(self):

        print(f'Tentando conectar com {self.host}:{self.port}...')
        self.sc.connect((self.host, self.port))
        print(f'Conectado com sucesso.\n')

        self.nome = input('Digite seu nome: ')
        print(f'\n Bem vindo {self.nome}!')

        #Criando as threads de envio e recebimento de mensagens

        envio = Envio(self.sc, self.nome)
        rec = Inbox(self.sc, self.nome)

        envio.start()
        rec.start()

        self.sc.sendall(f'\n{self.nome} entrou no chat.'.encode('UTF-8'))
        print('\rPara sair do chat, digite "QUIT"\n')
        print(f'{self.nome}: ', end='')

        return rec

    def send(self, textInput):

        mensagem = textInput.get()
        textInput.delete(0, tk.END)
        if mensagem:
            if self.mensagens:
                self.mensagens.insert(tk.END, f'{self.nome}: {mensagem}')

        if mensagem == 'QUIT':
            self.sc.sendall(f'{self.nome} saiu do chat.'.encode('UTF-8'))
            print('\nSaindo...')
            self.sc.close()
            os._exit(0)

        else:
            self.sc.sendall(f'{self.nome}: {mensagem}'.encode('UTF-8'))

def main(host, port):

    cliente = Cliente(host, port)
    rec = cliente.start()

    window = tk.Tk()
    window.title('Whatsapp 2')
    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    msgs = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    msgs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    cliente.mensagens = msgs
    rec.mensagens = msgs

    fromMessage.grid(row=0, column=0, columnspan=2, sticky='nsew')
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)
    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind('<Return>', lambda x: cliente.send(textInput))
    textInput.insert(0, '')

    btnSend = tk.Button(
        master=window,
        text='Enviar',
        command=lambda: cliente.send(textInput)
    )

    fromEntry.grid(row=1, column=0, padx=10,sticky='ew')
    btnSend.grid(row=1, column=1, padx=10,sticky='ew')

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1,minsize=200, weight=0)

    window.mainloop()


if __name__ == '__main__':
	
	

	main('localhost', 8000)



