import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the function to get user input
def get_user_input():
    in_adl_eat_encoded_options = {'自立': 2, '一部介助': 1, '全介助・不明': 0}
    in_adl_transfer_encoded_options = {'自立': 3, '軽度介助': 2, '高度介助': 1, '全介助・不明': 0}
    in_adl_dressing_encoded_options = {'自立': 1, '介助・不明': 0}
    in_adl_toilet_encoded_options = {'自立': 2, '一部介助': 1, '全介助・不明': 0}
    in_adl_walk_encoded_options = {'自立': 3, '1人介助': 2, '車椅子で自立': 1, '全介助・不明': 0}
    in_adl_stairs_encoded_options = {'自立': 2, '一部介助': 1, '全介助': 0}
    in_adl_clothes_encoded_options = {'自立': 2, '一部介助': 1, '全介助・不明': 0}
    in_adl_defecation_encoded_options = {'自立': 2, '時々失敗': 1, '全介助・不明': 0}
    in_adl_urination_encoded_options = {'自立': 2, '時々失敗': 1, '全介助・不明': 0}
    gender_options = {'男': 1, '女': 0}
    pathway_options = {'自宅': 1, '医療・福祉施設': 0}
    dialysis_options = {'透析あり': 0, '透析なし': 1}
    dementia_flag_options = {'認知症なし': 0, '認知症あり': 1}
    anesthesia_options = {'全身麻酔なし': 1, '全身麻酔あり': 0}
    first_jcs_options = {'1－1': 1, '1－2': 2, '1－3': 3, '2－10': 10, '2－20': 20, '2－30': 30, '3－100': 100, '3－200': 200, '3－300': 300}
    last_jcs_options = {'1－1': 1, '1－2': 2, '1－3': 3, '2－10': 10, '2－20': 20, '2－30': 30, '3－100': 100, '3－200': 200, '3－300': 300}
    ICD10_options = {'内分泌,栄養および代謝疾患': 0, '呼吸器系の疾患': 1, '妊娠,分娩および産褥': 2, '尿路性器系の疾患': 3, '循環器系の疾患': 4, '感染症および寄生虫症': 5, '損傷,中毒およびその他の外因の影響': 6, '新生物': 7, '消化器系の疾患': 8, '神経系の疾患': 9, '筋骨格系および結合組織の疾患': 10, '血液および造血器の疾患ならびに免疫機構の障害': 11, 'その他の疾患': 12}

    selected_in_adl_eat_encoded = st.sidebar.selectbox('ADLスコア：食事', list(in_adl_eat_encoded_options.keys()))
    selected_in_adl_transfer_encoded = st.sidebar.selectbox('ADLスコア：移乗', list(in_adl_transfer_encoded_options.keys()))
    selected_in_adl_dressing_encoded = st.sidebar.selectbox('ADLスコア：整容', list(in_adl_dressing_encoded_options.keys()))
    selected_in_adl_toilet_encoded = st.sidebar.selectbox('ADLスコア：トイレ動作', list(in_adl_toilet_encoded_options.keys()))
    selected_in_adl_walk_encoded = st.sidebar.selectbox('ADLスコア：歩行', list(in_adl_walk_encoded_options.keys()))
    selected_in_adl_stairs_encoded = st.sidebar.selectbox('ADLスコア：階段', list(in_adl_stairs_encoded_options.keys()))
    selected_in_adl_clothes_encoded = st.sidebar.selectbox('ADLスコア：更衣', list(in_adl_clothes_encoded_options.keys()))
    selected_in_adl_defecation_encoded = st.sidebar.selectbox('ADLスコア：排便', list(in_adl_defecation_encoded_options.keys()))
    selected_in_adl_urination_encoded = st.sidebar.selectbox('ADLスコア：排尿', list(in_adl_urination_encoded_options.keys()))
    selected_gender = st.sidebar.selectbox('性別', list(gender_options.keys()))
    selected_pathway = st.sidebar.selectbox('入院経路', list(pathway_options.keys()))
    selected_dialysis = st.sidebar.selectbox('透析の有無', list(dialysis_options.keys()))
    selected_dementia_flag = st.sidebar.selectbox('認知症の有無', list(dementia_flag_options.keys()))
    selected_anesthesia = st.sidebar.selectbox('全身麻酔の有無', list(anesthesia_options.keys()))
    selected_first_jcs = st.sidebar.selectbox('GICU初回介入時のJCS', list(first_jcs_options.keys()))
    selected_last_jcs = st.sidebar.selectbox('GICU最終介入時のJCS', list(last_jcs_options.keys()))
    selected_ICD10 = st.sidebar.selectbox('ICD10大項目', list(ICD10_options.keys()))

    new_data = {
        'in_adl_eat_encoded': in_adl_eat_encoded_options[selected_in_adl_eat_encoded],
        'in_adl_transfer_encoded': in_adl_transfer_encoded_options[selected_in_adl_transfer_encoded],
        'in_adl_dressing_encoded': in_adl_dressing_encoded_options[selected_in_adl_dressing_encoded],
        'in_adl_toilet_encoded': in_adl_toilet_encoded_options[selected_in_adl_toilet_encoded],
        'in_adl_walk_encoded': in_adl_walk_encoded_options[selected_in_adl_walk_encoded],
        'in_adl_stairs_encoded': in_adl_stairs_encoded_options[selected_in_adl_stairs_encoded],
        'in_adl_clothes_encoded': in_adl_clothes_encoded_options[selected_in_adl_clothes_encoded],
        'in_adl_defecation_encoded': in_adl_defecation_encoded_options[selected_in_adl_defecation_encoded],
        'in_adl_urination_encoded': in_adl_urination_encoded_options[selected_in_adl_urination_encoded],
        'df_in_adl_sum': st.sidebar.number_input('入院時のADLスコア合計', min_value=0, max_value=20, step=1),
        'first_fss': st.sidebar.number_input('GICU初回介入時FSS－ICU合計点', min_value=0, max_value=35, step=1),
        'last_fss': st.sidebar.number_input('GICU最終介入時FSS－ICU合計点', min_value=0, max_value=35, step=1),
        'first_gcs': st.sidebar.number_input('GICU初回介入時GCS合計点', min_value=2, max_value=15, step=1),
        'last_gcs': st.sidebar.number_input('GICU最終介入時GCS合計点', min_value=2, max_value=15, step=1),
        'first_jcs': first_jcs_options[selected_first_jcs],
        'last_jcs': last_jcs_options[selected_last_jcs],
        'first_ims': st.sidebar.number_input('GICU初回介入時IMS合計点', min_value=0, max_value=10, step=1),
        'last_ims': st.sidebar.number_input('GICU最終介入時IMS合計点', min_value=0, max_value=10, step=1),
        'first_mrc': st.sidebar.number_input('GICU初回介入時MRC合計点', min_value=0, max_value=60, step=1),
        'last_mrc': st.sidebar.number_input('GICU最終介入時MRC合計点', min_value=0, max_value=60, step=1),
        'first_rass': st.sidebar.number_input('GICU初回介入時RASS合計点', min_value=-5, max_value=4, step=1),
        'last_rass': st.sidebar.number_input('GICU最終介入時RASS合計点', min_value=-5, max_value=4, step=1),
        'first_sofa': st.sidebar.number_input('GICU初回介入時SOFAスコア合計点', min_value=0, max_value=24, step=1),
        'last_sofa': st.sidebar.number_input('GICU最終介入時SOFAスコア合計点', min_value=0, max_value=24, step=1),
        '性別_encoded': gender_options[selected_gender],
        '入院時年齢': st.sidebar.number_input('入院時年齢'),
        'ICD10大項目_encoded': ICD10_options[selected_ICD10],
        '入院経路_encoded': pathway_options[selected_pathway],
        'GICU入室までの日数': st.sidebar.number_input('入院からGICU入室までの日数'),
        'stay_gicu_length_x': st.sidebar.number_input('GICU在室日数'),
        '麻酔_encoded': anesthesia_options[selected_anesthesia],
        '出血量': st.sidebar.number_input('手術での出血量', min_value=0, step=1),
        'BMI': st.sidebar.number_input('BMI'),
        '喫煙指数': st.sidebar.number_input('喫煙指数'),
        '透析_encoded': dialysis_options[selected_dialysis],
        '認知症フラッグ_encoded': dementia_flag_options[selected_dementia_flag],
    }

    return pd.DataFrame(new_data, index=[0])

# Define the main function
def main():
    st.title('GICU入室患者の退院時ADL予測')

    # Get user input
    new_data = get_user_input()

    # Make prediction
    prediction = model.predict(new_data)

    # Display prediction
    if prediction[0] == 0:
        st.write('予測結果：ADL低下なし')
    elif prediction[0] == 1:
        st.write('予測結果：ADL低下あり')

# Run the main function
if __name__ == '__main__':
    main()
