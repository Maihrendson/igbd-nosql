"""
Módulo de compatibilidade com a convenção do projeto openf1.
Permite executar o pipeline utilizando: python api/datacollector.py
"""
import sys
from pathlib import Path

# Garante importação tanto rodando de cartola-api/ quanto de cartola-api/api/
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from cartola_etl import main
except ImportError:
    from api.cartola_etl import main

if __name__ == "__main__":
    sys.exit(main())
