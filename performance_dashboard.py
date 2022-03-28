# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 17:00:00 2022

@author: kamalap1
"""

import base64

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

pd.set_option('mode.chained_assignment', None)

st.set_page_config(layout='wide')
st.title('API - Performance Evolution Dashboard')
st.markdown('Developed & Maintained by: DS Data Applications Team')
st.markdown('Last updated data as of **_27th_ _March_ _2022_**.')
radio = st.sidebar.radio('Report Type:', ['Aggregate view', 'Breakdown per client (Selection by client name)',
                                          'Breakdown per client (selection by client username)', 'Breakdown per method group',
                                          'Breakdown per product'])

df = pd.read_excel(r"data_source.xlsx", sheet_name='GoldenSource')
# Considering last 16 weeks data only
df = df[df.Weektag.isin(
    sorted(list(df['Weektag'].value_counts().index))[-16:])].reset_index(drop=True)
# Calculated fields
df['Avg time x call (s)'] = df['ServerTime (m)']*60 / \
    (df['Successful calls']+df['Failed calls'])
df['Failure rate'] = df['Failed calls'] / \
    (df['Successful calls']+df['Failed calls'])
df['Product version'] = df['Product'].apply(
    lambda x: 'v4' if '4' in x else 'v3')


def calc_type(version, method):
    if version == 'v3' and method[:5] == 'REST.':
        return 'REST1 on v3'
    elif version == 'v4' and method[:5] == 'REST.':
        return 'REST1 on v4'
    elif method[:5] == 'REST2':
        return 'REST2'
    elif version == 'v3':
        return 'SOAP3'
    else:
        return 'SOAP4'


def calc_method(method):
    getdata = ['GetData', 'REST2.Companies.data', 'GetEngagementInfo', 'GetListData', 'REST.GetData', 'GetExchangeRate', 'REST2.Contacts.data', 'REST2.Companies.remoteaccess.data', 'REST2.news.data', 'GetLabels', 'REST2.bvdidshistory.data', 'GetAvailableAccountTypePreferences', 'GetAnalysisPDF', 'GetEngagementAnalyses',
               'GetPeerValue', 'GetReportSection', 'REST2.ContactsPortfolio.Data', 'REST2.CompaniesPortfolio.Data', 'REST2.Rates.data', 'REST2.CompaniesPortfolio.data.', 'GetAvailableSearches', 'GetEngagementPDF', 'REST2.Companies.data.', 'GetSavedSearches', 'REST2.Patents.data', 'GetAllEngagementsForLeadCompanyBvdId','REST2.Companies.data.Dashboard']
    match = ['Match', 'REST.Match', 'MatchWithCustomRules', 'REST2.companies.match',
             'REST2.companies.match.', 'REST2.companies.match.data.', 'MatchWithOwnData', 'MatchIdentifier']
    other = ['FindByRecordId', 'Find', 'FindByBVDId', 'ClearSelection', 'FindAnd', 'FindWithRecordSet', 'FindByName', 'UpdateMyDataTable', 'SetAccountTypePreference', 'CreateQueryExt', 'SetLanguage', 'FindFormula', 'CreateEngagement', 'DeleteEngagement', 'FindOr', 'CreateQueryFromListFormat', 'CreateQuery', 'CreateQuery2Ext', 'FindWithStrategy', 'REST2.Companies.Screening.ExternalWatchlist',
             'REST2.Companies.Metadata.ListFormat.AsQuery', 'GetRemainingBvDCredits', 'GetLabelsFromModel', 'GetAvailableSearchStepParameters', 'GetPeerGroupFromParameters', 'GetPeerValues', 'GetRecordsPeerGroup', 'FindNot', 'GetListFormatNames', 'REST2.companies.Metadata.ListFormat', 'REST2.Contacts.metadata.data.select', 'REST2.RemoteAccessController.Data', 'REST2.Companies.metadata.where', 'GetDecisionModels']
    ownership = ['GetCorporateGroup', 'REST2.ownership.ownershipexplorer.data', 'GetOwnershipStructure',
                 'REST2.Ownership.Pathfinder', 'GetBOIntegratedPercentage', 'REST2.Ownership.OwnershipExplorer', 'REST2.ownership.data','REST2.OwnershipExplorer']
    portfolio = ['REST2.Companies.CustomData.Add', 'REST2.CompaniesPortfolio.assessments', 'REST2.ContactsPortfolio.Portfolio', 'REST2.CompaniesPortfolio.portfolio', 'REST2.CompaniesPortfolio.assessments.Start', 'REST2.CompaniesPortfolio.Portfolio.Add', 'REST2.ContactsPortfolio.Portfolio.Add', 'REST2.RemoteAccessController.Portfolio', 'REST2.CompaniesPortfolio.CustomData.Add', 'REST2.ContactsPortfolio.assessments.Start', 'REST2.RemoteAccessController.Assessments',
                 'REST2.CompaniesPortfolio.assessments.Recalculate', 'REST2.CompaniesPortfolio.CustomData.Remove', 'REST2.CompaniesPortfolio.CustomData.Replace', 'REST2.RemoteAccessController.CustomData', 'REST2.ContactsPortfolio.assessments', 'REST2.ContactsPortfolio.CustomData.Add', 'REST2.ContactsPortfolio.CustomData.Remove', 'REST2.ContactsPortfolio.Portfolio.Remove', 'REST2.CompaniesPortfolio.Portfolio.Remove', 'REST2.CompaniesPortfolio.assessments.models', 'REST2.CompaniesPortfolio.customdata', 'CreateOwnEntity']
    recordset = ['AddBvDIdInRecordSet', 'AddBvD9InRecordSet', 'REST2.Companies.Store.RecordSets', 'REST2.companies.store.recordsets.add', 'RemoveRecordSet', 'AddRecordInRecordSet', 'REST2.Companies.Store.RecordSets.Add.CRMPRODBVDIds', 'REST2.Companies.Store.RecordSets.Add.CustomerData',
                 'RemoveBvDIDFromRecordSet', 'REST2.Companies.store.recordsets.add.SilexGalexLegacyRecordset', 'RemoveRecordFromRecordSet', 'REST2.Companies.Store.RecordSets.RPMRecordSet', 'REST2.Companies.Store.RecordSets.Add.EVSMonitoringPortfolio', 'REST2.Companies.Store.RecordSets.Add.RatingsPlus']
    if method.upper() in (name.upper() for name in getdata):
        return 'GetData'
    elif method.upper() in (name.upper() for name in match):
        return 'Match'
    elif method.upper() in (name.upper() for name in other):
        return 'Other'
    elif method.upper() in (name.upper() for name in ownership):
        return 'Ownership'
    elif method.upper() in (name.upper() for name in portfolio):
        return 'Portfolio'
    elif method.upper() in (name.upper() for name in recordset):
        return 'RecordSet'
    else:
        return ''


df['Type'] = df[['Product version', 'method']].apply(
    lambda x: calc_type(*x), axis=1)
df['Method grouping'] = df['method'].apply(lambda x: calc_method(x))

# Charting
aggregate = df.groupby('Weektag')[
    ['ServerTime (m)', 'Successful calls', 'Failed calls']].sum()
aggregate['Avg time x call (s)'] = aggregate['ServerTime (m)'] * \
    60/(aggregate['Successful calls']+aggregate['Failed calls'])
aggregate['Failure rate'] = (
    aggregate['Failed calls']/(aggregate['Successful calls']+aggregate['Failed calls']))*100
aggregate = aggregate.reset_index()
sum_df = pd.DataFrame([str(round(float(aggregate[-1:]['Successful calls'])/1000000, 2))+'M', str(round(float(aggregate[-2:]['Successful calls'].pct_change()[-1:]*100), 1)),
                           str(round(float(aggregate[-1:]['Failed calls'])/1000, 2))+'K', str(round(float(aggregate[-2:]['Failed calls'].pct_change()[-1:]*100), 1))]).T
sum_df.columns = ['Sum of successful calls W',
                      'Change from W-1 to W(%)', 'Sum of failed calls W', 'Change from W-1 to W (%)']
avg_df = pd.DataFrame([str(round(float(aggregate[-1:]['Avg time x call (s)']), 2)), str(round(float(aggregate[-2:]['Avg time x call (s)'].pct_change()[-1:]*100), 1)),
                           str(round(float(aggregate[-1:]['Failure rate']), 2)), str(round(float(aggregate[-2:]['Failure rate'].pct_change()[-1:]*100), 1))]).T
avg_df.columns = [
        'Avg time per call (s) W', 'Change from W-1 to W(%)', 'Failure rate W', 'Change from W-1 to W (%)']
aggregate = aggregate.round(2)        
if radio == r'Aggregate view':
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Successful calls'], text=aggregate['Successful calls'],
                   name='Sum of Successful calls', marker_color='rgb(226, 170, 0)', textangle=0))
    fig1.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Failed calls'], text=aggregate['Failed calls'],
                   name='Sum of Failed calls', marker_color='rgb(255, 209, 132)', textangle=0))
    fig1.update_traces(texttemplate='%{text:.3s}')
    fig1.update_layout(title='Aggregate view', barmode='stack')
    st.plotly_chart(fig1)
    st.write(sum_df.reset_index(drop=True))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Avg time x call (s)'], text=aggregate['Avg time x call (s)'],
                  name='Average time per call(s)', textposition='outside', marker_color='rgb(68, 114, 196)'))
    fig.add_trace(go.Scatter(x=aggregate.Weektag,
                  y=aggregate['Failure rate'], mode='lines+markers', name='Failure rate', marker_color='rgb(237, 125, 49)'))
    fig.update_traces(texttemplate='%{text:.3s}')
    st.plotly_chart(fig)
    # st.markdown('**Summary Report - {}:**'.format('Aggregate view'))
    st.write(avg_df.reset_index(drop=True))
# Download Raw Data
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="raw_data.csv">Download Raw Data</a>'
    st.markdown(href, unsafe_allow_html=True)

elif radio == r'Breakdown per client (Selection by client name)':
    client_name = st.multiselect('Select the client name', list(
        sorted(df.ClientName.unique())), [])
    if st.button('Submit'):
        st.write('**You selected:**', client_name)
        client_df = df[df.ClientName.isin(client_name)]
        aggregate = client_df.groupby(
            'Weektag')[['ServerTime (m)', 'Successful calls', 'Failed calls']].sum()
        aggregate['Avg time x call (s)'] = aggregate['ServerTime (m)']*60/(
            aggregate['Successful calls']+aggregate['Failed calls'])
        aggregate['Failure rate'] = (
            aggregate['Failed calls']/(aggregate['Successful calls']+aggregate['Failed calls']))*100
        aggregate = aggregate.reset_index().round(2)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Avg time x call (s)'], text=aggregate['Avg time x call (s)'],
                      name='Average time per call(s)', textposition='outside', marker_color='rgb(68, 114, 196)'))
        fig.add_trace(go.Scatter(x=aggregate.Weektag,
                      y=aggregate['Failure rate'], mode='lines+markers', name='Failure rate', marker_color='rgb(237, 125, 49)'))
        # fig.update_traces(texttemplate='%{text:.3s}')
        fig.update_layout(title='Aggregate view')
        st.plotly_chart(fig)
        avg_df = pd.DataFrame([str(round(float(aggregate[-1:]['Avg time x call (s)']), 2)), str(round(float(aggregate[-2:]['Avg time x call (s)'].pct_change()[-1:]*100), 1)),
                               str(round(float(aggregate[-1:]['Failure rate']), 2)), str(round(float(aggregate[-2:]['Failure rate'].pct_change()[-1:]*100), 1))]).T
        avg_df.columns = [
            'Avg time per call (s) W', 'Change from W-1 to W(%)', 'Failure rate W', 'Change from W-1 to W (%)']
        # st.markdown('**Summary Report - {}:**'.format('Aggregate view'))
        st.write(avg_df.reset_index(drop=True))

        client_df = client_df.groupby(by=['Weektag', 'Method grouping'])[
            ['Successful calls']].sum().reset_index()
        fig1 = go.Figure(data=[
            go.Bar(name='GetData', x=client_df[client_df['Method grouping'] == 'GetData']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'GetData']['Successful calls'], marker_color='rgb(86, 135, 54)'),
            go.Bar(name='Match', x=client_df[client_df['Method grouping'] == 'Match']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Match']['Successful calls'], marker_color='rgb(104, 162, 66)'),
            go.Bar(name='Other', x=client_df[client_df['Method grouping'] == 'Other']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Other']['Successful calls'], marker_color='rgb(144, 187, 122)'),
            go.Bar(name='Ownership', x=client_df[client_df['Method grouping'] == 'Ownership']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Ownership']['Successful calls'], marker_color='rgb(190, 213, 180)'),
            go.Bar(name='Portfolio', x=client_df[client_df['Method grouping'] == 'Portfolio']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Portfolio']['Successful calls'], marker_color='rgb(216, 230, 210)'),
            go.Bar(name='RecordSet', x=client_df[client_df['Method grouping'] == 'RecordSet']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'RecordSet']['Successful calls'], marker_color='rgb(232, 240, 228)')

        ])
        # Change the bar mode
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1)
        prop_df = pd.DataFrame(client_df.groupby(
            'Method grouping')['Successful calls'].sum())
        prop_df['Proportion (%)'] = (
            prop_df['Successful calls']/prop_df['Successful calls'].sum()*100).astype(int)
        prop_df.rename(
            columns={'Successful calls': 'Sum of Successful calls'}, inplace=True)
        st.write(prop_df.sort_values(
            by='Proportion (%)', ascending=False).reset_index())

elif radio == r'Breakdown per client (selection by client username)':
    client_name = st.multiselect(
        'Select the client username', list(sorted(df.UserName.unique())), [])
    if st.button('Submit'):
        st.write('**You selected:**', client_name)
        client_df = df[df.UserName.isin(client_name)]
        aggregate = client_df.groupby(
            'Weektag')[['ServerTime (m)', 'Successful calls', 'Failed calls']].sum()
        aggregate['Avg time x call (s)'] = aggregate['ServerTime (m)']*60/(
            aggregate['Successful calls']+aggregate['Failed calls'])
        aggregate['Failure rate'] = (
            aggregate['Failed calls']/(aggregate['Successful calls']+aggregate['Failed calls']))*100
        aggregate = aggregate.reset_index().round(2)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Avg time x call (s)'], text=aggregate['Avg time x call (s)'],
                      name='Average time per call(s)', textposition='outside', marker_color='rgb(68, 114, 196)'))
        fig.add_trace(go.Scatter(x=aggregate.Weektag,
                      y=aggregate['Failure rate'], mode='lines+markers', name='Failure rate', marker_color='rgb(237, 125, 49)'))
        # fig.update_traces(texttemplate='%{text:.3s}')
        fig.update_layout(title='Aggregate view')
        st.plotly_chart(fig)
        avg_df = pd.DataFrame([str(round(float(aggregate[-1:]['Avg time x call (s)']), 2)), str(round(float(aggregate[-2:]['Avg time x call (s)'].pct_change()[-1:]*100), 1)),
                               str(round(float(aggregate[-1:]['Failure rate']), 2)), str(round(float(aggregate[-2:]['Failure rate'].pct_change()[-1:]*100), 1))]).T
        avg_df.columns = [
            'Avg time per call (s) W', 'Change from W-1 to W(%)', 'Failure rate W', 'Change from W-1 to W (%)']
        # st.markdown('**Summary Report - {}:**'.format('Aggregate view'))
        st.write(avg_df.reset_index(drop=True))

        client_df = client_df.groupby(by=['Weektag', 'Method grouping'])[
            ['Successful calls']].sum().reset_index()
        fig1 = go.Figure(data=[
            go.Bar(name='GetData', x=client_df[client_df['Method grouping'] == 'GetData']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'GetData']['Successful calls'], marker_color='rgb(86, 135, 54)'),
            go.Bar(name='Match', x=client_df[client_df['Method grouping'] == 'Match']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Match']['Successful calls'], marker_color='rgb(104, 162, 66)'),
            go.Bar(name='Other', x=client_df[client_df['Method grouping'] == 'Other']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Other']['Successful calls'], marker_color='rgb(144, 187, 122)'),
            go.Bar(name='Ownership', x=client_df[client_df['Method grouping'] == 'Ownership']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Ownership']['Successful calls'], marker_color='rgb(190, 213, 180)'),
            go.Bar(name='Portfolio', x=client_df[client_df['Method grouping'] == 'Portfolio']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'Portfolio']['Successful calls'], marker_color='rgb(216, 230, 210)'),
            go.Bar(name='RecordSet', x=client_df[client_df['Method grouping'] == 'RecordSet']['Weektag'],
                   y=client_df[client_df['Method grouping'] == 'RecordSet']['Successful calls'], marker_color='rgb(232, 240, 228)')

        ])
        # Change the bar mode
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1)
        prop_df = pd.DataFrame(client_df.groupby(
            'Method grouping')['Successful calls'].sum())
        prop_df['Proportion (%)'] = (
            prop_df['Successful calls']/prop_df['Successful calls'].sum()*100).astype(int)
        prop_df.rename(
            columns={'Successful calls': 'Sum of Successful calls'}, inplace=True)
        st.write(prop_df.sort_values(
            by='Proportion (%)', ascending=False).reset_index())

elif radio == r'Breakdown per method group':
    client_name = st.multiselect('Select the Method group', list(
        sorted(df['Method grouping'].unique())), [])
    if st.button('Submit'):
        st.write('**You selected:**', client_name)
        client_df = df[df['Method grouping'].isin(client_name)]
        aggregate = client_df.groupby(
            'Weektag')[['ServerTime (m)', 'Successful calls', 'Failed calls']].sum()
        aggregate['Avg time x call (s)'] = aggregate['ServerTime (m)']*60/(
            aggregate['Successful calls']+aggregate['Failed calls'])
        aggregate['Failure rate'] = (
            aggregate['Failed calls']/(aggregate['Successful calls']+aggregate['Failed calls']))*100
        aggregate = aggregate.reset_index().round(2)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Avg time x call (s)'], text=aggregate['Avg time x call (s)'],
                      name='Average time per call(s)', textposition='outside', marker_color='rgb(68, 114, 196)'))
        fig.add_trace(go.Scatter(x=aggregate.Weektag,
                      y=aggregate['Failure rate'], mode='lines+markers', name='Failure rate', marker_color='rgb(237, 125, 49)'))
        # fig.update_traces(texttemplate='%{text:.3s}')
        fig.update_layout(title='Aggregate view')
        st.plotly_chart(fig)
        avg_df = pd.DataFrame([str(round(float(aggregate[-1:]['Avg time x call (s)']), 2)), str(round(float(aggregate[-2:]['Avg time x call (s)'].pct_change()[-1:]*100), 1)),
                               str(round(float(aggregate[-1:]['Failure rate']), 2)), str(round(float(aggregate[-2:]['Failure rate'].pct_change()[-1:]*100), 1))]).T
        avg_df.columns = [
            'Avg time per call (s) W', 'Change from W-1 to W(%)', 'Failure rate W', 'Change from W-1 to W (%)']
        # st.markdown('**Summary Report - {}:**'.format('Aggregate view'))
        st.write(avg_df.reset_index(drop=True))

        temp_df = df[df['Method grouping'].isin(["GetData"])]
        prop_df = pd.DataFrame(temp_df.groupby(['ClientName'])[
                               'Successful calls'].sum())
        prop_df['Proportion (%)'] = (
            prop_df['Successful calls']/prop_df['Successful calls'].sum()*100).astype(int)
        prop_df = prop_df.sort_values(
            by='Proportion (%)', ascending=False).reset_index()
        temp_df = df[df.ClientName.isin(prop_df[:10]['ClientName'])]
        client_df = temp_df.groupby(by=['Weektag', 'ClientName'])[
            ['Successful calls']].sum().reset_index()
        fig = go.Figure()
        for client_name in prop_df[:10]['ClientName']:
            fig.add_trace(go.Bar(name=client_name, x=client_df[client_df['ClientName'] == client_name]
                          ['Weektag'], y=client_df[client_df['ClientName'] == client_name]['Successful calls']))
        # Change the bar mode
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)
        prop_df.rename(
            columns={'Successful calls': 'Sum of Successful calls'}, inplace=True)
        st.write(prop_df.sort_values(by='Proportion (%)',
                 ascending=False).reset_index(drop=True))

else:
    product = st.multiselect('Select the product', list(
        sorted(df.Product.unique())), [])
    if st.button('Submit'):
        st.write('**You selected:**', product)
        client_df = df[df.Product.isin(product)]
        aggregate = client_df.groupby(
            'Weektag')[['ServerTime (m)', 'Successful calls', 'Failed calls']].sum()
        aggregate['Avg time x call (s)'] = aggregate['ServerTime (m)']*60/(
            aggregate['Successful calls']+aggregate['Failed calls'])
        aggregate['Failure rate'] = (
            aggregate['Failed calls']/(aggregate['Successful calls']+aggregate['Failed calls']))*100
        aggregate = aggregate.reset_index().round(2)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=aggregate.Weektag, y=aggregate['Avg time x call (s)'], text=aggregate['Avg time x call (s)'],
                      name='Average time per call(s)', textposition='outside', marker_color='rgb(68, 114, 196)'))
        fig.add_trace(go.Scatter(x=aggregate.Weektag,
                      y=aggregate['Failure rate'], mode='lines+markers', name='Failure rate', marker_color='rgb(237, 125, 49)'))
        fig.update_layout(title='Aggregate view')
        st.plotly_chart(fig)
        avg_df = pd.DataFrame([str(round(float(aggregate[-1:]['Avg time x call (s)']), 2)), str(round(float(aggregate[-2:]['Avg time x call (s)'].pct_change()[-1:]*100), 1)),
                               str(round(float(aggregate[-1:]['Failure rate']), 2)), str(round(float(aggregate[-2:]['Failure rate'].pct_change()[-1:]*100), 1))]).T
        avg_df.columns = [
            'Avg time per call (s) W', 'Change from W-1 to W(%)', 'Failure rate W', 'Change from W-1 to W (%)']
        st.write(avg_df.reset_index(drop=True))
