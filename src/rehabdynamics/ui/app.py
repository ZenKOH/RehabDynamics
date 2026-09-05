from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from rehabdynamics.io.opensim import OpenSimFormatError, parse_mot
from rehabdynamics.pipeline import analyse_trial

st.set_page_config(page_title="RehabDynamics", layout="wide")
st.title("RehabDynamics")
st.caption("Uncertainty-aware movement intelligence for rehabilitation research")
st.warning(
    "Research use only. Not a medical device. "
    "Do not use outputs for diagnosis or treatment decisions."
)

uploaded = st.file_uploader("OpenSim motion file (.mot)", type=["mot", "sto", "txt"])
pathology = st.text_input("Pathology / cohort (optional)", placeholder="e.g. stroke")
assistive = st.text_input("Assistive device / condition (optional)", placeholder="e.g. exoskeleton")

if uploaded:
    try:
        trial = parse_mot(
            StringIO(uploaded.getvalue().decode("utf-8")),
            metadata={"pathology": pathology, "assistive_device": assistive},
        )
        result = analyse_trial(trial, reference_config=Path("configs/reference_envelope.yaml"))
        status = result.ood.status.upper()
        st.subheader(f"Safety screen: {status}")
        st.write(result.ood.model_dump())

        c1, c2, c3 = st.columns(3)
        c1.metric("Duration", f"{result.trial_metrics.get('duration_s', 0):.2f} s")
        sr = result.trial_metrics.get("sample_rate_hz")
        c2.metric("Sample rate", "n/a" if sr is None else f"{sr:.1f} Hz")
        speed = result.trial_metrics.get("forward_speed_m_s")
        c3.metric("Pelvis forward speed", "n/a" if speed is None else f"{speed:.2f} m/s")

        candidate = [
            column
            for column in trial.kinematics.columns
            if any(term in column for term in ("hip", "knee", "ankle"))
        ][:8]
        if candidate:
            long = pd.concat([trial.time.rename("time"), trial.kinematics[candidate]], axis=1).melt(
                id_vars="time", var_name="coordinate", value_name="value"
            )
            figure = px.line(long, x="time", y="value", color="coordinate")
            st.plotly_chart(figure, use_container_width=True)
        with st.expander("Machine-readable result"):
            st.json(result.model_dump(mode="json"))
    except (UnicodeDecodeError, OpenSimFormatError, ValueError) as exc:
        st.error(str(exc))
