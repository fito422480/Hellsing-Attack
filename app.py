
import streamlit as st
import pandas as pd
import plotly.express as px
from nocturne import port_scan, http_flood, tcp_flood, slowloris_attack, ddos_attack
from language import t, Config

def main():
    st.set_page_config(page_title="Hellsing Attack", page_icon="ðŸ”¥", layout="wide")

    st.title("Hellsing Attack")
    st.markdown(t.get('warning'))
    st.markdown(t.get('warning_legal'))

    st.sidebar.title(t.get('settings_title'))
    language = st.sidebar.selectbox(t.get('current_language'), ["english", "spanish"])
    if language != Config.LANGUAGE:
        Config.LANGUAGE = language
        Config.save_config()
        st.rerun()

    st.sidebar.title(t.get('select_attack'))
    attack_type = st.sidebar.selectbox("",
                                     [t.get('port_scan'), t.get('http_flood'), t.get('tcp_flood'), t.get('slowloris'),
                                      t.get('ddos_sim')])

    if attack_type == t.get('port_scan'):
        st.header(t.get('port_scan_title'))
        target = st.text_input(t.get('enter_ip_or_domain'))
        start_port = st.number_input(t.get('start_port_prompt'), 1, 65535, 1)
        end_port = st.number_input(t.get('end_port_prompt'), 1, 65535, 10000)

        if st.button(t.get('port_scan')):
            if target:
                with st.spinner(t.get('scanning_ports').format(start_port, end_port, target)):
                    open_ports = port_scan(target, start_port, end_port)
                st.success(t.get('scan_completed').format(open_ports))
                if open_ports:
                    df = pd.DataFrame(open_ports, columns=["Port"])
                    st.dataframe(df)
            else:
                st.error(t.get('error_no_target'))

    elif attack_type == t.get('http_flood'):
        st.header(t.get('http_flood_title'))
        target = st.text_input(t.get('enter_url'))
        num_requests = st.number_input(t.get('num_requests_prompt'), 1, 1000000, 1000)
        delay = st.number_input(t.get('delay_prompt'), 0.0, 10.0, 0.1, 0.1)

        if st.button(t.get('http_flood')):
            if target:
                with st.spinner(t.get('starting_http_flood').format(target)):
                    results = http_flood(target, num_requests, delay)
                st.success("Attack finished!")
                st.json(results)
            else:
                st.error(t.get('error_no_target'))

    elif attack_type == t.get('tcp_flood'):
        st.header(t.get('tcp_flood_title'))
        target = st.text_input(t.get('enter_ip'))
        port = st.number_input(t.get('port_prompt'), 1, 65535, 80)
        num_connections = st.number_input(t.get('num_connections_prompt'), 1, 10000, 100)
        message = st.text_input(t.get('message_prompt'))

        if st.button(t.get('tcp_flood')):
            if target:
                with st.spinner(t.get('starting_tcp_flood').format(target, port)):
                    results = tcp_flood(target, port, num_connections, message)
                st.success("Attack finished!")
                st.json(results)
            else:
                st.error(t.get('error_no_target'))

    elif attack_type == t.get('slowloris'):
        st.header(t.get('slowloris_title'))
        target = st.text_input(t.get('enter_url'))
        num_sockets = st.number_input(t.get('num_sockets_prompt'), 1, 1000, 150)

        if st.button(t.get('slowloris')):
            if target:
                with st.spinner(t.get('starting_slowloris').format(target)):
                    results = slowloris_attack(target, num_sockets)
                st.success(results["message"])
            else:
                st.error(t.get('error_no_target'))

    elif attack_type == t.get('ddos_sim'):
        st.header(t.get('ddos_title'))
        target = st.text_input(t.get('enter_url'))
        duration = st.number_input(t.get('duration_prompt'), 1, 3600, 60)

        if st.button(t.get('ddos_sim')):
            if target:
                with st.spinner(t.get('starting_ddos').format(target, duration)):
                    results = ddos_attack(target, duration)
                st.success("Attack finished!")
                st.json(results)
            else:
                st.error(t.get('error_no_target'))

if __name__ == '__main__':
    main()
