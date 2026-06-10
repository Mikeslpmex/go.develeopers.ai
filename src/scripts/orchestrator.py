#!/usr/bin/env python3
import os
import json
from datetime import datetime
from typing import Dict

class DeployOrchestrator:
    def __init__(self):
        self.plataformas = {
            "render": {
                "costo": 0.0,           # actualiza manualmente o con API
                "uptime": 99.8,
                "velocidad_webhook": "alta",
                "limite_free": "bueno",
                "puntuacion": 0
            },
            "railway": {
                "costo": 0.0,
                "uptime": 99.5,
                "velocidad_webhook": "media",
                "limite_free": "excelente",
                "puntuacion": 0
            },
            "flyio": {
                "costo": 0.0,
                "uptime": 99.7,
                "velocidad_webhook": "alta",
                "limite_free": "medio",
                "puntuacion": 0
            }
        }
        self.historico = []

    def actualizar_metricas(self, plataforma: str, costo: float, uptime: float, latencia: float):
        if plataforma in self.plataformas:
            self.plataformas[plataforma]["costo"] = costo
            self.plataformas[plataforma]["uptime"] = uptime
            # Calcular puntuación simple
            score = (uptime * 0.5) + (1 / (costo + 0.01) * 30) - (latencia * 0.2)
            self.plataformas[plataforma]["puntuacion"] = round(score, 2)

    def recomendar_mejor_plataforma(self) -> Dict:
        mejor = max(self.plataformas.items(), key=lambda x: x[1]["puntuacion"])
        return {"plataforma": mejor[0], **mejor[1]}

    def guardar_historico(self):
        self.historico.append({
            "fecha": datetime.now().isoformat(),
            "plataformas": self.plataformas.copy()
        })
        with open("deploy_history.json", "w") as f:
            json.dump(self.historico, f, indent=2)

# Uso
orq = DeployOrchestrator()
orq.actualizar_metricas("render", costo=5, uptime=99.9, latencia=120)
orq.actualizar_metricas("railway", costo=4, uptime=99.4, latencia=180)

print("Recomendación:", orq.recomendar_mejor_plataforma())
