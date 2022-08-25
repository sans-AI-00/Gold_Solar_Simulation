import simulation_functions
import plotting
from global_variables import *
import streamlit as st
import pandas as pd
import statistics


def simulation_values_and_plots(monthly_consumption, hours_of_activity, kwp=3, orientation=None, tilt=None, loc=LOC_1,
                                max_charging_power=2, max_discharge_power=2, battery_capacity=5):

    production_history = simulation_functions.production_history(kwp=kwp, orientation=orientation, tilt=tilt, loc=loc)

    total_energy = 0
    for i in range(len(production_history)):
        for j in range(len(production_history[i])):
            total_energy += production_history[i][j]

    consumption_history = simulation_functions.consumption_history(monthly_consumption, hours_of_activity)

    result = simulation_functions.simulation(production_history, consumption_history, max_charging_power=max_charging_power,
                                             max_discharge_power=max_discharge_power, battery_capacity=battery_capacity)

    color_list = ['blue', 'blue', 'green', 'red', 'orange', 'yellow', 'green']
    ec_list = ['black', 'black', 'black', 'black', 'black', 'black', 'black']
    ylabel_list = ['energia accumulata (Kwh)', 'inserire titolo', 'energia autoconsumata (Kwh)', 'consumo esterno (Kwh)',
                   'consumo totale (Kwh)', 'energia prodotta (Kwh)', 'energia immessa in rete (Kwh)']
    title_list = ['Energia accumulata mensilmente', 'inserire etichetta asse y', 'Energia autoconsumata mensilmente', 'Consumo esterno mensile',
                   'Consumo totale mensile', 'Energia prodotta mensilmente', 'Energia immessa in rete mensilmente']

    plots = []
    for i in range(len(result['monthly'])):
        plot = plotting.hist_plot(result['monthly'][i], ylabel=ylabel_list[i], title=title_list[i], color=color_list[i], ec=ec_list[i])
        plot.savefig(f'hist/fig_{i}.png')
        plots.append(plot)

    return {'plots': plots, 'monthly': result['monthly'], 'annual': result['annual']}


def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value
########################################################################################################################
########################################################################################################################


def main():

    st.set_page_config(page_title="Simulazione Gold Solar", page_icon="icona.png")

    # Persistent state
    set_state_if_absent("kwp", 4)
    set_state_if_absent("loc", LOC_1)
    set_state_if_absent("max_charging_power", 2)
    set_state_if_absent("max_discharge_power", 2)
    set_state_if_absent("battery_capacity", 5)
    set_state_if_absent("monthly_consumption", [500 for i in range(12)])
    set_state_if_absent("average_monthly_consumption", 500)
    set_state_if_absent("hours_of_activity", [{'start': 8, 'stop': 24} for i in range(12)])

    st.sidebar.image("GOLD-SOLAR-LOGO_3.png", caption=None, width=None, use_column_width=True, clamp=False,
                     channels="RGB", output_format="auto")

    st.sidebar.markdown("""<hr />""", unsafe_allow_html=True)
    st.session_state.kwp = st.sidebar.number_input(label="Taglia dell'impianto (Kwp)", min_value=0,
                                                   max_value=None, value=4, step=1)
    st.sidebar.markdown("""<hr />""", unsafe_allow_html=True)
    st.sidebar.markdown("""<p style='text-align:center;padding: 0 0 1rem;'>sistema di accumulo</p>""",
                unsafe_allow_html=True)
    st.session_state.max_charging_power = st.sidebar.number_input(label="Potenza massima di carica (Kw/h)", min_value=0,
                                                                  max_value=None, value=2, step=1)
    st.session_state.max_discharge_power = st.sidebar.number_input(label="Potenza massima di scarica (Kw/h)", min_value=0,
                                                                   max_value=None, value=2, step=1)
    st.session_state.battery_capacity = st.sidebar.number_input(label="Capacità (Kwh)", min_value=0,
                                                                max_value=None, value=5, step=1)
    st.sidebar.markdown("""<hr />""", unsafe_allow_html=True)
    st.session_state.average_monthly_consumption = st.sidebar.number_input(label="Consumo mensile medio (Kwh)", min_value=0,
                                                                           max_value=None, value=500, step=1)
    st.sidebar.markdown("""<hr />""", unsafe_allow_html=True)
    loc_options = ('Napoli', 'Roma')
    loc_option = st.sidebar.selectbox(label="Località (provincia)", options=loc_options, index=0)
    st.sidebar.markdown("""<hr />""", unsafe_allow_html=True)
    st.sidebar.markdown("""<p style='text-align:center;padding: 0 0 1rem;'>© 2022 by Gold Solar s.r.l</p>""",
                unsafe_allow_html=True)

    if loc_option == 'Napoli':
        st.session_state.loc = LOC_1
    elif loc_option == 'Roma':
        st.session_state.loc = LOC_2

    st.session_state.monthly_consumption = [st.session_state.average_monthly_consumption for i in range(12)]

    kwp = st.session_state['kwp']
    loc = st.session_state['loc']
    max_charging_power = st.session_state['max_charging_power']
    max_discharge_power = st.session_state['max_discharge_power']
    battery_capacity = st.session_state['battery_capacity']
    monthly_consumption = st.session_state['monthly_consumption']
    hours_of_activity = st.session_state['hours_of_activity']

    result = simulation_values_and_plots(monthly_consumption, hours_of_activity, kwp=kwp, orientation=None, tilt=None, loc=loc,
                                         max_charging_power=max_charging_power, max_discharge_power=max_discharge_power,
                                         battery_capacity=battery_capacity)

    plots = result['plots']
    monthly = result['monthly']
    annual = result['annual']

    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Energia accumulata mensilmente</h3>""",
                unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[0])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia massima accumulata: {round(max(monthly[0]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia minima accumulata: {round(min(monthly[0]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia media accumulata: {round(statistics.mean(monthly[0]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia totale accumulata: {round(annual[0],2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[0]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}
        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Energia autoconsumata mensilmente</h3>""",
                unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[2])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia massima autoconsumata: {round(max(monthly[2]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia minima autoconsumata: {round(min(monthly[2]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia media autoconsumata: {round(statistics.mean(monthly[2]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia totale autoconsumata: {round(annual[2],2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[2]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}
        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Consumo esterno mensile</h3>""",
                unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[3])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo esterno massimo: {round(max(monthly[3]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo esterno minimo: {round(min(monthly[3]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo esterno medio: {round(statistics.mean(monthly[3]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo esterno totale: {round(annual[3],2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[3]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}
        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto mensile</h3>""",
                unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[4])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto massimo: {round(max(monthly[4]), 2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto minimo: {round(min(monthly[4]), 2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto medio: {round(statistics.mean(monthly[4]), 2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto totale: {round(annual[4], 2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[4]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}
        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Energia prodotta mensilmente</h3>""",
                unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[5])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia massima prodotta: {round(max(monthly[5]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia minima prodotta: {round(min(monthly[5]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia media prodotta: {round(statistics.mean(monthly[5]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia prodotta totale: {round(annual[5],2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[5]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}
        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<h3 style='text-align:center;padding: 0 0 1rem;'>Energia immessa in rete mensilmente</h3>""",
                unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        col1.pyplot(plots[6])
        col2.markdown(f"""<br/>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia massima immessa: {round(max(monthly[6]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia minima immessa: {round(min(monthly[6]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia media immessa: {round(statistics.mean(monthly[6]),2)} Kwh</p>
                         <p style='text-align:center;padding: 0 0 1rem;'>Energia immessa totale: {round(annual[6],2)} Kwh</p>
                         <br/>
                         <br/>""",
                      unsafe_allow_html=True)
        monthly_data = monthly[6]
        d = {'Gen': [round(monthly_data[0], 2)], 'Feb': [round(monthly_data[1], 2)], 'Mar': [round(monthly_data[2], 2)],
             'Apr': [round(monthly_data[3], 2)], 'Mag': [round(monthly_data[4], 2)], 'Giu': [round(monthly_data[5], 2)],
             'Lug': [round(monthly_data[6], 2)], 'Ago': [round(monthly_data[7], 2)], 'Set': [round(monthly_data[8], 2)],
             'Ott': [round(monthly_data[9], 2)], 'Nov': [round(monthly_data[10], 2)], 'Dic': [round(monthly_data[11], 2)]}

        df = pd.DataFrame(data=d, index=['Energia'])
        st.dataframe(data=df, width=None, height=None)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align:center;padding: 0 0 1rem;'>Riepilogo</h3>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Energia totale accumulata: {round(annual[0],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Energia totale autoconsumata: {round(annual[2],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Consumo esterno totale: {round(annual[3],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Consumo assoluto totale: {round(annual[4],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Energia prodotta totale: {round(annual[5],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Energia immessa totale: {round(annual[6],2)} Kwh</h5>""",
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align:center;padding: 0 0 1rem;'>Autosufficienza: {round(annual[2]/annual[4],2) * 100}%</h5>""",
                unsafe_allow_html=True)
    st.markdown("""<hr />""", unsafe_allow_html=True)
    st.markdown("""<p style='text-align:center;padding: 0 0 1rem;'>© 2022 by Gold Solar s.r.l</p>""",
                unsafe_allow_html=True)

main()


