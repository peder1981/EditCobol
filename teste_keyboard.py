#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import keyboard

print("Testando captura de teclas. Pressione 'q' para sair.")

try:
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(f"Tecla pressionada: {event.name}")
            if event.name == 'q':
                break
except KeyboardInterrupt:
    print("\nTeste interrompido pelo usuário.")
print("Teste concluído.")
