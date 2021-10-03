import sys, pygame, socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
targetAddress = "10.18.221.18" #whatever the IP of the server is
port = 5005

pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

forward = False
backward = False
left = False
right = False
binary = [0, 0, 0, 0]

run = True

previous = -1

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                binary[2] = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                binary[3] = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                binary[0] = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                binary[1] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                binary[2] = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                binary[3] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                binary[0] = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                binary[1] = 0

        num = 0
        for b in binary:
            num = 2 * num + b
        if(num != previous):
            print(num)
            sock.sendto(num.to_bytes(2,"big"), (targetAddress, port))
        previous = num

    pygame.display.flip()