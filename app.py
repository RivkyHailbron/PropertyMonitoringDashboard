import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(layout="wide", page_title="APN 2654002037 Dashboard")

# Property title
st.title(" Property Status Dashboard")
st.subheader("Asset APN: 2654002037")

try:
    # Load data from the JSON file
    with open("inspections_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data['inspections'])

    # CSV download button
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="📥 Download Data Report (Excel/CSV)", data=csv,
                       file_name='Report_APN_2654002037.csv', mime='text/csv')

    # KPIs
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total", len(df))
    m2.metric("New", len(df[df['status'] == 'New']))
    m3.metric("Open", len(df[df['status'] == 'Open']))
    m4.metric("In Progress", len(df[df['status'] == 'In Progress']))
    m5.metric("Urgent (HIGH)", len(df[df['urgency'] == 'HIGH']))
    m6.metric("Closed", len(df[df['status'] == 'Closed']))

    st.markdown("---")

    # Visuals
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Distribution by Status")
        all_s = ["Closed", "In Progress", "Open", "New"]
        counts = df['status'].value_counts().reindex(all_s, fill_value=0).reset_index()
        fig_pie = px.pie(counts, names='status', values='count', hole=0.5,
                         color='status', color_discrete_map={
                "New": "#636EFA", "In Progress": "#EF553B", "Open": "#00CC96", "Closed": "#AB63FA"})
        st.plotly_chart(fig_pie, width='stretch')

    with c2:
        st.subheader("Urgency Analysis (In Progress)")
        u_df = df[df['status'] == "In Progress"]
        u_counts = u_df['urgency'].value_counts().reindex(["HIGH", "LOW"], fill_value=0).reset_index()
        fig_bar = px.bar(u_counts, x='urgency', y='count', color='urgency',
                         color_discrete_map={"HIGH": "#D32F2F", "LOW": "#FFC107"})
        st.plotly_chart(fig_bar, width='stretch')

    st.markdown("---")

    # Case Explorer with tabs and filtering
    st.subheader("Case Explorer")
    tab_titles = ["ALL", "NEW", "OPEN", "IN PROGRESS (ALL)", "IN PROGRESS HIGH", "IN PROGRESS LOW", "CLOSED"]
    tabs = st.tabs(tab_titles)

    def get_filtered(title):
        if title == "NEW": return df[df['status'] == "New"]
        if title == "OPEN": return df[df['status'] == "Open"]
        if title == "IN PROGRESS (ALL)": return df[df['status'] == "In Progress"]
        if title == "IN PROGRESS HIGH": return df[(df['status'] == "In Progress") & (df['urgency'] == "HIGH")]
        if title == "IN PROGRESS LOW": return df[(df['status'] == "In Progress") & (df['urgency'] == "LOW")]
        if title == "CLOSED": return df[df['status'] == "Closed"]
        return df

    for i, tab in enumerate(tabs):
        title = tab_titles[i]
        with tab:
            f_df = get_filtered(title)
            st.write(f"Showing {len(f_df)} records:")
            sel = st.dataframe(f_df[['case_number', 'case_type', 'status', 'urgency', 'complaint_nature']],
                               use_container_width=True, hide_index=True, on_select="rerun",
                               selection_mode="single-row", key=f"tbl_{title}")

            if len(sel.selection.rows) > 0:
                c_no = f_df.iloc[sel.selection.rows[0]]['case_number']
                full_item = next(item for item in data['inspections'] if item['case_number'] == c_no)
                st.markdown(f"#### Case Details: {c_no}")
                st.info(f"**Nature:** {full_item.get('complaint_nature', 'N/A')}")
                st.dataframe(pd.DataFrame(full_item.get('flow', [])), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Waiting for data: {e}")