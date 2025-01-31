# Test for å hente data fra en graf i Amplitude.

# Funksjonen under er hentet fra gamle team IA: https://github.com/navikt/ia-key-metrics/blob/main/main.py
# Dette er nå arkivert, og selv om det pleide å funke, jeg fikk ikke til å kjøre det lokalt nå, får timeout.
# Har gitt tilgang til naisjobben til å bruke proxyen her: https://github.com/navikt/reops-proxy/blob/master/.nais/prod-gcp.yaml
# Spør i #amplitude om dere trenger hjelp.
# Om dere får det til, slett denne filen :)

import pandas as pd
import requests

def hent_antall_besøkende_siste_30_dager():
    # TODO: Bruk ingress lokalt
    # "https://reops-proxy.intern.nav.no/amplitude/api/3/chart/e-czvqr8g/query"
    response = requests.get(
        "http://reops-proxy.team-researchops/amplitude/api/3/chart/e-czvqr8g/query"
    )

    if not response.ok:
        return "NaN"

    body = response.json()

    besøkende = body["data"]["series"][0]
    datoer = pd.to_datetime(body["data"]["xValues"])

    dagens_dato = pd.to_datetime("today")
    startdato = dagens_dato - pd.DateOffset(days=30)

    siste_30_dager = pd.DataFrame(data=besøkende, index=datoer)["value"][
        startdato:dagens_dato
    ]

    return siste_30_dager.sum()