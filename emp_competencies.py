import streamlit as st
import pandas as pd


st.title('Analisis Kompetensi Pegawai')
st.write("Hasil analisis data kesesuaian kompetensi pegawai dengan history pelatihan yang sudah diikuti:")

data = pd.read_pickle('hasil_perhitungan.pkl')
data_pelatihan = pd.read_csv('list_pelatihan.csv').set_index('nama')

expander = st.expander("Disclaimer")
expander.write("1. Data masih membutuhkan analisis yang lebih dalam.")
expander.write("2. Tidak untuk digunakan sebagai dasar utama pengambilan keputusan")

st.sidebar.write("## Pilih data yang ingin divisualisasikan:")

col2s = st.sidebar.columns(2)

jabatan_based = st.sidebar.checkbox("Data berdasarkan jabatan", value=True)
individual_based = st.sidebar.checkbox("Data detil individu")
st.markdown("---")
if jabatan_based:
    jabatan = st.selectbox("Pilih Jabatan:", data.nama.unique())

    list_pelatihan = data[data.nama==jabatan].list_pelatihan.to_list()[0]
    st.write("Pelatihan yang diperlukan: ")
    st.write(list_pelatihan)

    index = (data[data.nama==jabatan].index)
    filtered_jabatan = data.loc[index].iloc[:,4:].T
    filtered_jabatan.columns = ['nama']
    filtered_jabatan = filtered_jabatan.sort_values(by='nama', ascending=False)
    filtered_jabatan['nama'] = round(filtered_jabatan['nama'] * 100, 0)


    container = st.container()

    for d in range(len(filtered_jabatan[:10])):
        col1, col2, col3 = st.columns([2,4,1])
        col1.write(filtered_jabatan.index[d])
        col2.progress(int(filtered_jabatan.nama[d]))
        col3.write(f"{filtered_jabatan.nama[d]}%")

    export_data = filtered_jabatan.to_csv().encode('utf-8')

    st.markdown("---")
    st.download_button("Unduh Data", data=export_data, file_name="test.csv")

if individual_based:
    nama = st.text_input("Ketik nama pegawai: ", value="Eko Supriyono")

    filtered_individu = data[['nama', nama]].sort_values(by=nama, ascending=False).reset_index(drop=True)
    filtered_individu[nama] = round(filtered_individu[nama] * 100, 0)

    for d in range(len(filtered_individu[:5])):
        col1, col2, col3 = st.columns([2,4,1])
        col1.write(filtered_individu['nama'][d])
        col2.progress(int(filtered_individu[nama][d]))
        col3.write(f"{filtered_individu[nama][d]}%")

    st.write(f"### History pelatihan {nama}:")

    pelatihan_pegawai = data_pelatihan.loc[[nama], 'list_pelatihan'].to_list()

    nomor = 1

    for i in eval(pelatihan_pegawai[0]): ## eval is unsafe in production
        st.write(f"{nomor}. {i}")
        nomor += 1
