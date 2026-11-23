import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title='CatalogFix AI – Demo', page_icon='📦', layout='wide')
st.title('📦 CatalogFix AI')
st.caption('Product data quality checks | Prototype – no AI rewriting yet')
st.info('Demo only. Do not upload confidential customer data. Files are processed during the session; no database is configured.')

sample = pd.DataFrame([
    {'sku':'A-001','title':'Blue Cotton T-Shirt','description':'100% cotton','price':'19.90'},
    {'sku':'A-002','title':'','description':'Soft everyday shirt','price':'24.90'},
    {'sku':'A-001','title':'Red Hoodie','description':'','price':'39.90'},
    {'sku':'A-004','title':'Green Socks','description':'Pair of socks','price':'-5'},
    {'sku':'A-005','title':'Black Cap','description':'Adjustable cap','price':'not available'},
])
st.download_button('Download sample CSV', sample.to_csv(index=False).encode('utf-8'), 'sample_products.csv', 'text/csv')
upload = st.file_uploader('Upload a CSV with sku, title, description, price', type=['csv'])
if upload is not None:
    try:
        df = pd.read_csv(upload, dtype=str, keep_default_na=False, encoding='utf-8-sig')
    except Exception as exc:
        st.error(f'Could not read CSV: {exc}')
        st.stop()
    df.columns = df.columns.str.strip().str.lower()
    required = ['sku','title','description','price']
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error('Missing columns: ' + ', '.join(missing))
        st.stop()
    if len(df) > 100:
        st.warning('Demo is limited to the first 100 products.')
        df = df.head(100).copy()
    if df.empty:
        st.warning('The file contains no products.')
        st.stop()
    sku = df['sku'].str.strip()
    title = df['title'].str.strip()
    description = df['description'].str.strip()
    price_raw = df['price'].str.strip().str.replace(',', '.', regex=False)
    price = pd.to_numeric(price_raw, errors='coerce')
    df['missing_sku'] = sku.eq('')
    df['duplicate_sku'] = sku.ne('') & sku.duplicated(keep=False)
    df['missing_title'] = title.eq('')
    df['missing_description'] = description.eq('')
    df['invalid_price'] = price.isna() | price.le(0)
    checks = ['missing_sku','duplicate_sku','missing_title','missing_description','invalid_price']
    df['issue_count'] = df[checks].sum(axis=1)
    a,b,c = st.columns(3)
    a.metric('Products checked', len(df))
    b.metric('Products with issues', int(df['issue_count'].gt(0).sum()))
    c.metric('Total issues found', int(df['issue_count'].sum()))
    st.subheader('Audit results')
    st.dataframe(df, use_container_width=True)
    st.download_button('Download audit CSV', df.to_csv(index=False).encode('utf-8-sig'), 'catalogfix_audit.csv', 'text/csv')
    st.caption('Checks are rule-based. Prices are assumed to be in a consistent currency; no currency conversion is performed.')
