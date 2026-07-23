import time
import sys

def main():
    distro = sys.argv[1] if len(sys.argv) > 1 else "desconocida"
    print(f"Iniciando herramienta para la distribución: {distro}...")
    time.sleep(2)  # Simulando trabajo
    print("La herramienta ha finalizado su trabajo con éxito.")
    
if __name__ == "__main__":
    main()
