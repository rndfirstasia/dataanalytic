import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import plost
from streamlit_gsheets import GSheetsConnection

#Layout
st.set_page_config(page_title="Data Analytic", page_icon="icon.png")

#df
#df = pd.read_excel('data_leader.xlsx')

# File upload widget in Streamlit
#uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

#if uploaded_file is not None:
    #df = pd.read_excel(uploaded_file)
    # Now you can use the DataFrame 'df' as needed
    #st.write(df)

#conn
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Sheet1")

#Sidebar
st.sidebar.title('Filter')
bins= [0,24,40,56,75, np.inf]
labels = ['Gen Z', 'Milenials', 'Gen X', 'Baby Boomer', 'Silent']
df['generasi'] = pd.cut(df['UMUR'], bins=bins, labels=labels, right=False)
selected_generations = st.sidebar.multiselect('Pilih generasi', labels, default=labels)
df = df[df['generasi'].isin(selected_generations)]

#Dataframe
st.title('Data Tarikan')
df

def get_median(series):
    return np.median(series)

def get_mode(series):
    values, counts = np.unique(series, return_counts=True)
    index = np.argmax(counts)
    return values[index]

def get_mean(series):
    return np.mean(series)

def get_std(series):
    return np.std(series, ddof=1)

def get_variance(series):
    return np.var(series, ddof=1)

def get_range(series):
    return np.ptp(series)

def get_quartiles(series):
    return np.percentile(series, [25, 50, 75])

def get_skewness(series):
    n = len(series)
    mean = np.mean(series)
    std = np.std(series, ddof=1)
    skewness = (np.sum((series - mean) ** 3) / n) / (std ** 3)
    return skewness

def get_kurtosis(series):
    n = len(series)
    mean = np.mean(series)
    std = np.std(series, ddof=1)
    kurtosis = (np.sum((series - mean) ** 4) / n) / (std ** 4) - 3
    return kurtosis

descriptive = {
    'Median' : [get_median(df['IQ']), get_median(df['S']), get_median(df['T']), get_median(df['A']), get_median(df['G']), get_median(df['E'])],
    'Mode' : [get_mode(df['IQ']), get_mode(df['S']), get_mode(df['T']), get_mode(df['A']), get_mode(df['G']), get_mode(df['E'])],
    'Mean' : [get_mean(df['IQ']), get_mean(df['S']), get_mean(df['T']), get_mean(df['A']), get_mean(df['G']), get_mean(df['E'])],
    'Std' : [get_std(df['IQ']), get_std(df['S']), get_std(df['T']), get_std(df['A']), get_std(df['G']), get_std(df['E'])],
    'Var' : [get_variance(df['IQ']), get_variance(df['S']), get_variance(df['T']), get_variance(df['A']), get_variance(df['G']), get_variance(df['E'])],
    'Range' : [get_range(df['IQ']), get_range(df['S']), get_range(df['T']), get_range(df['A']), get_range(df['G']), get_range(df['E'])],
    'Percentile 25' : [get_quartiles(df['IQ'])[0], get_quartiles(df['S'])[0], get_quartiles(df['T'])[0], get_quartiles(df['A'])[0], get_quartiles(df['G'])[0], get_quartiles(df['E'])[0]],
    'Percentile 50' : [get_quartiles(df['IQ'])[1], get_quartiles(df['S'])[1], get_quartiles(df['T'])[1], get_quartiles(df['A'])[1], get_quartiles(df['G'])[1], get_quartiles(df['E'])[1]],
    'Percentile 75' : [get_quartiles(df['IQ'])[2], get_quartiles(df['S'])[2], get_quartiles(df['T'])[2], get_quartiles(df['A'])[2], get_quartiles(df['G'])[2], get_quartiles(df['E'])[2]],
    'Skew' : [get_skewness(df['IQ']), get_skewness(df['S']), get_skewness(df['T']), get_skewness(df['A']), get_skewness(df['G']), get_skewness(df['E'])],
    'Kurt' : [get_kurtosis(df['IQ']), get_kurtosis(df['S']), get_kurtosis(df['T']), get_kurtosis(df['A']), get_kurtosis(df['G']), get_kurtosis(df['E'])]
}

desc_df = pd.DataFrame(descriptive, index=['IQ', 'S', 'T', 'A', 'G', 'E'])

st.title('Descriptive Stats')
st.write(len(df))

st.table(desc_df)

#IQ
st.title('Graph Distribusi IQ')
st.write("""
## Perbandingan Histogram IQ dan IQ Ori

Dengan membandingkan kedua histogram, kita dapat mengamati perbedaan antara skor yang telah dikalibrasi oleh Assessor dan skor asli, memberikan wawasan tentang seberapa signifikan dampak penyesuaian yang dilakukan oleh Assessor terhadap distribusi skor IQ.

1. **IQ (Adjusted Intelligence Quotient)**:
Histogram ini akan menampilkan frekuensi skor IQ setelah dilakukan penyesuaian oleh seorang assessor. Penyesuaian yang dilakukan menyesuaikan dengan buku kasus. Hasilnya adalah skor yang dianggap lebih mewakili kemampuan intelektual individu dalam kondisi penilaian yang telah disempurnakan.

2. **IQ Ori (Original Intelligence Quotient)**:
Histogram ini menampilkan frekuensi dari skor IQ asli tanpa penyesuaian, yang berasal langsung dari hasil tes peserta. Skor ini mencerminkan performa individu berdasarkan kriteria dan standar tes yang telah ditetapkan, tanpa memasukkan koreksi atau penilaian tambahan dari seorang assessor.
""")

fig, ax = plt.subplots(1,2)
sns.histplot(df['IQ'], kde=True, ax=ax[0])
ax[0].set_title('IQ')

sns.histplot(df['IQOri'], kde=True, ax=ax[1])
ax[1].set_title('IQ Ori')

st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="iq_text_area")

#STAGE
st.title('Graph Distribusi STAGE')
st.write("""
Analisis histogram kepribadian STAGE memperlihatkan bagaimana skor individu berdistribusi di lima domain utama:

1. **Stability**: Berhubungan dengan kontrol emosi dan ketahanan stres.
2. **Tenacity**: Mengukur tingkat kesadaran, organisasi, dan bertanggung jawab.
3. **Adaptability**: Menunjukkan kreativitas, keingintahuan, dan penerimaan terhadap pengalaman baru.
4. **Genuineness**: Refleksi dari keramahan, empati, dan perilaku kooperatif.
5. **Extraversion**: Menilai energi sosial dan kecenderungan untuk berinteraksi dengan orang lain.

Dengan membandingkan histogram-histogram ini, kita dapat menggambarkan variasi dalam lima aspek kunci STAGE dalam database.
""")

fig, ax = plt.subplots(3, 2, figsize=(15, 10))

sns.histplot(df['S'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi S')

sns.histplot(df['T'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi T')

sns.histplot(df['A'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi A')

sns.histplot(df['G'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi G')

sns.histplot(df['E'], kde=True, ax=ax[2, 0])
ax[2, 0].set_title('Distribusi E')

ax[2, 1].remove()
plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="stage_text_area")

#Agility
st.title('Agility Index')
st.write("""
Agility (ketangkasan) adalah kemampuan untuk memahami keadaan dengan cepat dan beradaptasi atau menyesuaikan diri secara efektif di dalamnya. Semakin tinggi Agility Index seseorang, menunjukkan kemudahan bagi dirinya untuk mengatasi kondisi yang dinamis di pekerjaan dan perusahaan.
""")

fig, ax = plt.subplots(3, 2, figsize=(15, 10))

sns.histplot(df['People Agility'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi People Agi')

sns.histplot(df['Mental Agility'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Mental Agi')

sns.histplot(df['Self-Awareness'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Self-Awareness')

sns.histplot(df['Result Agility'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Result Agi')

sns.histplot(df['Change Agility'], kde=True, ax=ax[2, 0])
ax[2, 0].set_title('Distribusi Change Agi')

sns.histplot(df['Agility Profile Score'], kde=True, ax=ax[2, 1])
ax[2, 1].set_title('Distribusi Skor Agility')

plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="agility_text_area")

#Stage Facet - Stability
st.title('Facet Stability')
st.write("""
Berikut adalah distribusi dari facet stability:
""")

fig, ax = plt.subplots(2, 2, figsize=(15, 10))

sns.histplot(df['S1'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi Facet Worry')

sns.histplot(df['S2'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Facet Calmness')

sns.histplot(df['S3'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Facet Optimism')

sns.histplot(df['S4'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Facet Recovery')

plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="stability_text_area")

#Stage Facet - Tenacity
st.title('Facet Tenacity')
st.write("""
Berikut adalah distribusi dari facet tenacity:
""")

fig, ax = plt.subplots(3, 2, figsize=(15, 10))

sns.histplot(df['T1'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi Facet Excellence')

sns.histplot(df['T2'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Facet Systematic')

sns.histplot(df['T3'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Facet Achievement Drive')

sns.histplot(df['T4'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Facet Attentiveness')

sns.histplot(df['T5'], kde=True, ax=ax[2, 0])
ax[2, 0].set_title('Distribusi Facet Deliberation')

ax[2, 1].remove()
plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="tenacity_text_area")

#Stage Facet - Adaptability
st.title('Facet Adaptability')
st.write("""
Berikut adalah distribusi dari facet adaptability:
""")

fig, ax = plt.subplots(2, 2, figsize=(15, 10))

sns.histplot(df['A1'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi Facet Altruism')

sns.histplot(df['A2'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Facet Compliance')

sns.histplot(df['A3'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Facet Modesty')

sns.histplot(df['A4'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Facet Assertiveness')

plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="adaptability_text_area")

#Stage Facet - Genuineness
st.title('Facet Genuineness')
st.write("""
Berikut adalah distribusi dari facet genuineness:
""")

fig, ax = plt.subplots(2, 2, figsize=(15, 10))

sns.histplot(df['G1'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi Facet Innovation')

sns.histplot(df['G2'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Facet Complexity')

sns.histplot(df['G3'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Facet Flexibility')

sns.histplot(df['G4'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Facet Wideness')

plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="genuineness_text_area")

#Stage Facet - Extraversion
st.title('Facet Extraversion')
st.write("""
Berikut adalah distribusi dari facet extraversion:
""")

fig, ax = plt.subplots(3, 2, figsize=(15, 10))

sns.histplot(df['E1'], kde=True, ax=ax[0, 0])
ax[0, 0].set_title('Distribusi Facet Friendliness')

sns.histplot(df['E2'], kde=True, ax=ax[0, 1])
ax[0, 1].set_title('Distribusi Facet Gregariousness')

sns.histplot(df['E3'], kde=True, ax=ax[1, 0])
ax[1, 0].set_title('Distribusi Facet Energy')

sns.histplot(df['E4'], kde=True, ax=ax[1, 1])
ax[1, 1].set_title('Distribusi Facet Leading Incharge')

sns.histplot(df['E5'], kde=True, ax=ax[2, 0])
ax[1, 0].set_title('Distribusi Facet Trust')

sns.histplot(df['E6'], kde=True, ax=ax[2, 1])
ax[1, 1].set_title('Distribusi Facet Courtesy')

plt.tight_layout()
st.pyplot(fig)
st.text_area(label="Tambahkan Analisa:", key="extraversion_text_area")
