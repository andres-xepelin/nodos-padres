import pandas as pd
import numpy as np

df = pd.read_csv('scripts/data.csv')

def get_parent_dataframe(rfc, dataframe=df):
    '''
    Returns a dataframe containing the info of a parent node.
    '''
    return dataframe[dataframe['parent'] == rfc]


def get_n_children(rfc):
    '''
    Returns the number of children of a parent node.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    n_children = temp_df['child'].nunique()
    
    return n_children


def get_parentTotalAmountFinanced(rfc):
    '''
    Returns the parent's total financed amount.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    parent_totalAmountFinanced = temp_df.parentTotalAmountFinanced.mean()

    return parent_totalAmountFinanced


def get_childTotalAmountFinanced(rfc):
    '''
    Returns the children's total financed amount.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    children_totalAmountFinanced = round(float(temp_df.childTotalAmountFinanced.sum()), 2)

    return children_totalAmountFinanced


def get_nodalTotalFinancedAmount(rfc):
    '''
    Returns the nodal's total financed amount (parent + children).
    '''
    return get_parentTotalAmountFinanced(rfc) + get_childTotalAmountFinanced(rfc)


def get_parentRevenue(rfc):
    '''
    Returns the parent's total revenue.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    parent_Revenue = temp_df.parentAmountRevenue.mean()

    return parent_Revenue


def get_childRevenue(rfc):
    '''
    Returns the children's total revenue.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    children_Revenue = round(float(temp_df.childAmountRevenue.sum()), 2)

    return children_Revenue


def get_nodalRevenue(rfc):
    '''
    Returns the nodal's total revenue (parent + children).
    '''
    return get_parentRevenue(rfc) + get_childRevenue(rfc)


def get_parentRateFD(rfc):
    '''
    Returns the parent's weighed average RateFD.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    parent_RateFD = temp_df.parentRateFD.mean()

    return parent_RateFD


def get_weightedAvgRate(rateCol, amountCol, dataframe=df):
    '''
    Returns the weighted average rate.
    '''
    temp_df = dataframe[[rateCol, amountCol]]
    
    temp_df.dropna(inplace=True)
    
    temp_df['totalAmount'] = temp_df[amountCol].sum()
    temp_df['weight'] = temp_df[amountCol] / temp_df['totalAmount']
    temp_df['weightedRate'] = temp_df[rateCol] * temp_df['weight']
        
    weighted_average_rate = temp_df['weightedRate'].sum()
    
    return weighted_average_rate


def get_childRateFD(rfc):
    '''
    Returns the children's weighed average RateFD.
    '''
    temp_df = get_parent_dataframe(rfc)
    
    children_RateFD = get_weightedAvgRate('childRateFD', 'childTotalAmountFinanced', temp_df)

    return children_RateFD


def get_nodalRateFD(rfc):
    '''
    Returns the nodal's (parent + children) weighed average RateFD.
    '''
    rates = [get_parentRateFD(rfc), get_childRateFD(rfc)]
    amounts = [get_parentTotalAmountFinanced(rfc), get_childTotalAmountFinanced(rfc)]
    
    d = {'rate': rates, 'amount': amounts}
    temp_df = pd.DataFrame(data=d, index=['parent', 'children'])
        
    return get_weightedAvgRate('rate', 'amount', temp_df)


def build_summary_row(rfc):
    '''
    Returns a row of a DataFrame with the parent and its metrics.
    '''
    
    d = {
        'parent':rfc,
        'children':get_n_children(rfc),
        'parentTotalAmountFinanced':get_parentTotalAmountFinanced(rfc),
        'childTotalAmountFinanced':get_childTotalAmountFinanced(rfc),
        'nodalTotalFinancedAmount':get_nodalTotalFinancedAmount(rfc),
        'parentRevenue':get_parentRevenue(rfc),
        'childRevenue':get_childRevenue(rfc),
        'nodalRevenue':get_nodalRevenue(rfc),
        'parentRateFD':get_parentRateFD(rfc),
        'childRateFD':get_childRateFD(rfc),
        'nodalRateFD':get_nodalRateFD(rfc)
    }

    row = pd.DataFrame(data=d, index=[0])
    
    return row


def get_summary(dataframe=df):
    '''
    Returns a DataFrame with all businesses and their KPIs.
    '''
    temp_df = pd.DataFrame()

    all_companies = np.union1d(df.parent.unique(), df.child.unique())
    
    for ii in all_companies:
        temp_df = pd.concat([temp_df, build_summary_row(ii)])    
    
    return temp_df