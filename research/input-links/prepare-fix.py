from pathlib import Path
P=Path('work/input-links');P.mkdir(exist_ok=True)
s=Path('work/input-v2/inputs.asm').read_text(encoding='utf-8')
s=s.replace(' clr.l (0x04,A3)\n move.w #0xd501',' clr.l (0x04,A3)\n clr.b (0x0d,A3)\n clr.b (0x0e,A3)\n clr.b (0x0f,A3)\n move.w #0xd501',1)
s=s.replace(' move.b D0,(0x05,A3)\n move.b (0xb6,A0)', ' move.b D0,(0x05,A3)\n clr.b (0x0e,A3)\n move.b (0xb6,A0)',1)
s=s.replace('command_ready:\n move.b D7,(0xb9,A0)', '''command_ready:
 ; Retener solo comandos reconocidos durante un basico de pie.
 ; No cancelar aqui: esperar al despacho natural o al asistente existente.
 clr.b (0x0e,A3)
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @queue_ready
 btst.b #0x04,(0x1e,A0)
 bne.w @queue_ready
 cmpi.w #0x0400,(A0)
 bcc.w @queue_program
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @queue_ready
 tst.b (0x0f,A3)
 beq.w @queue_ready
 bra.w @queue_store
queue_program:
 cmpi.w #0x0800,(A0)
 bcc.w @queue_ready
queue_store:
 move.b D7,(0x0d,A3)
 move.b #0x06,(0x0e,A3)
queue_ready:
 move.b D7,(0xb9,A0)''',1)
s=s.replace('matcher_done:\n .hex 46df', '''matcher_done:
 ; Seis actualizaciones maximas. Un golpe recibido, cambio de sentido,
 ; vuelo o tecnica iniciada descartan la orden. Solo reemitir en neutral.
 tst.b (0x0e,A3)
 beq.w @queue_done
 tst.w (0x24,A0)
 beq.w @queue_clear
 btst.b #0x04,(0x1e,A0)
 bne.w @queue_clear
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @queue_clear
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @queue_clear
 cmpi.w #0x0800,(A0)
 bcc.w @queue_clear
 subq.b #0x01,(0x0e,A3)
 cmpi.b #0xff,(0xb9,A0)
 bne.w @queue_done
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @queue_done
 move.b (0x0d,A3),(0xb9,A0)
 bra.w @queue_done
queue_clear:
 clr.b (0x0e,A3)
queue_done:
 ; Recordar un basico en la lectura anterior: la rutina nativa puede
 ; finalizarlo antes de que el reconocedor vea el boton de este frame.
 clr.b (0x0f,A3)
 cmpi.w #0x0400,(A0)
 bcs.w @queue_exit
 cmpi.w #0x0800,(A0)
 bcc.w @queue_exit
 move.b #0x01,(0x0f,A3)
queue_exit:
 .hex 46df''',1)
(P/'inputs.asm').write_text(s,encoding='utf-8')
java=Path('work/scripts/AssembleBasicChains.java').read_text().replace('AssembleBasicChains','AssembleInputLinks').replace('base=0x3dd000','base=0x3de000');Path('work/scripts/AssembleInputLinks.java').write_text(java)
ps=Path('work/input-v2/assemble.ps1').read_text().replace('AssembleInputV2.java','AssembleInputLinks.java');(P/'assemble.ps1').write_text(ps)
