# iAquaponics
# Popis aplikace
Aplikace iAquaponics je určena k řízení systému akvaponie pomocí Raspberry Pi. Řídí dvě čerpadla a dvě lampy prostřednictvím GPIO pinů na Raspberry Pi. Aplikace funguje podle předdefinované logiky pro mokré/suché cykly čerpadel a světelné cykly pro lampy.

# Hlavní funkce aplikace
## Řízení čerpadel:
Pumpa 1 (In4): Přenáší vodu z akvária do záhonu. Čerpadlo se zapíná na 3 minuty a poté je vypnuto na 57 minut.
Pumpa 2 (In2): Přenáší vodu ze záhonu zpět do akvária. Čerpadlo se zapíná na 6 minut a poté je vypnuto na 54 minut.
Mezi aktivací Pumpy 1 a Pumpy 2 je 10 minutová pauza, aby záhon zůstal 10 minut ve vodě.
## Řízení lamp:
Lampa záhonu (In3): Aktivní od 7:00 do 21:00 (denní cyklus).
~~Lampa akvária (In4): Aktivní od 8:00 do 17:00.~~
## Čisté ukončení aplikace:
Aplikace se stará o to, aby při přerušení (např. při KeyboardInterrupt nebo při signálu SIGTERM) byly všechny GPIO piny správně uvolněny.
### Jak to funguje?
#### Zachytávání přerušení: Aplikace aktivně sleduje signály, které mohou vést k jejímu ukončení. Konkrétně se jedná o:
- `KeyboardInterrupt`: Tento signál je vyvolán, když uživatel manuálně ukončí program pomocí kombinace kláves `Ctrl+C`.
- `SIGTERM`: Tento signál může být odeslán například při ukončení procesu přes příkaz `kill`

# Spuštění aplikace:
1. Použijte webove rozhraní https://www.raspberrypi.com/software/connect/, otevřete terminál buď samostatně nebo přes možnost "screen sharing".
2. Navugujte do složky - `cd projects/relay_module`, v ní se má nachazet script `iAquaponics.py`
3. Spusťte aplikaci v režimu nohup, aby mohla běžet na pozadí, vratí vam PID procesu, ten můžete pak použit na  zabítí procesu
`nohup python3 iAquaponics.py > stdout.log 2>&1 &`
# Zkontrolujte, zda aplikace běží:
`ps aux | grep python3`
# Zastavení aplikace:
## Najděte PID procesu:
` ps aux | grep python3 `
## Ukončete aplikaci:
`kill <PID>`

# Zkontrolujte soubor stdout.log pro výstup z aplikace:
`cat stdout.log`
Chcete-li zobrazit obsah souboru stdout.log v reálném čase, můžete použít příkaz: 
`tail -f stdout.log`






