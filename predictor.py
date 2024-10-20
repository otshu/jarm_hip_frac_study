import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('model_jarm_hip_frac_study.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the function to get user input
def get_user_input():
    受傷前の活動性_options = {'杖なし歩行': 0, '一本杖で外出可能': 1, '歩行補助具を使用して外出可能': 2, '屋内のみ歩行可能 / 介助なしには外出不能': 3, '歩行不能': 4}
    術前全身状態_options = {'（手術となる原因以外は）健康な患者': 0, '軽度・中等度の全身疾患をもつ患者': 1, '重度の全身疾患をもつ患者': 2, '生命を脅かすような重度の全身疾患をもつ患者': 3}
    骨折のタイプ1_options = {'転位型大腿骨頚部骨折である': 1, '転位型大腿骨頚部骨折ではない': 0}
    骨折のタイプ2_options = {'大腿骨転子部骨折（頚基部骨折を含む）である': 1, '大腿骨転子部骨折（頚基部骨折を含む）ではない': 0}
    手術法_options = {'髄内釘が施行された': 1, '髄内釘が施行されていない': 0}

    selected_受傷前の活動性 = st.sidebar.selectbox('受傷前の活動性', list(受傷前の活動性_options.keys()))
    selected_術前全身状態 = st.sidebar.selectbox('術前全身状態', list(術前全身状態_options.keys()))
    selected_骨折のタイプ1 = st.sidebar.selectbox('骨折のタイプ1', list(骨折のタイプ1_options.keys()))
    selected_骨折のタイプ2 = st.sidebar.selectbox('骨折のタイプ2', list(骨折のタイプ2_options.keys()))
    selected_手術法 = st.sidebar.selectbox('手術法', list(手術法_options.keys()))

    new_data = {
        '2.02 受傷前の活動性': 受傷前の活動性_options[selected_受傷前の活動性],
        '2.04 術前全身状態　ASA grade': 術前全身状態_options[selected_術前全身状態],
        '2.07 骨折のタイプ_2. 転位型大腿骨頚部骨折': 骨折のタイプ1_options[selected_骨折のタイプ1],
        '2.07 骨折のタイプ_3. 大腿骨転子部骨折（頚基部骨折を含む）': 骨折のタイプ2_options[selected_骨折のタイプ2],
        '3.03 手術法_4. 髄内釘': 手術法_options[selected_手術法],
        '体重': st.sidebar.number_input('体重', min_value=0, step=0.1),
        'sum_of_digits': st.sidebar.number_input('入院時ADLスコア合計点', min_value=0, step=1),
        'BMI': st.sidebar.number_input('BMI', min_value=0, step=0.1),
        '入院-手術時間': st.sidebar.number_input('入院-手術時間（分）', min_value=0, step=1),
        '1.04 受傷時年齢': st.sidebar.number_input('受傷時年齢', min_value=0, step=1),
        '2.03 術前 簡易認知テスト(AMTS)': st.sidebar.number_input('術前簡易認知テスト点数', min_value=0, max_value=10, step=1),
        '入院時Alb値': st.sidebar.number_input('入院時Alb値', min_value=0, step=0.1),
    }

    return pd.DataFrame(new_data, index=[0])

# Define the main function
def main():
    st.title('大腿骨近位部骨折患者の術後2週時点での歩行自立予測')

    # Get user input
    new_data = get_user_input()

    # Make prediction
    prediction = model.predict(new_data)

    # Display prediction
    if prediction[0] == 0:
        st.write('予測結果：歩行自立可能')
    elif prediction[0] == 1:
        st.write('予測結果：歩行自立困難')

# Run the main function
if __name__ == '__main__':
    main()
