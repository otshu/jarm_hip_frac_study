import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

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

    # Get user input for height and weight
    weight = st.sidebar.number_input('体重 (kg)', min_value=0.0, step=0.1)
    height = st.sidebar.number_input('身長 (cm)', min_value=0.0, step=0.1)

    # Calculate BMI (height in meters)
    if height > 0:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
    else:
        bmi = 0.0

    # 入院日時と手術開始日時を入力
    admission_date = st.sidebar.date_input('入院日')
    admission_time = st.sidebar.time_input('入院時間')
    surgery_date = st.sidebar.date_input('手術日')
    surgery_time = st.sidebar.time_input('手術時間')

    # datetimeオブジェクトを作成
    admission_datetime = datetime.combine(admission_date, admission_time)
    surgery_datetime = datetime.combine(surgery_date, surgery_time)

    # 入院-手術時間（分）を計算
    time_difference = (surgery_datetime - admission_datetime).total_seconds() / 60
    if time_difference < 0:
        st.sidebar.error('手術開始日時が入院日時よりも前になっています。正しい日時を入力してください。')
        time_difference = 0  # 負の値を防ぐため

    new_data = {
        '体重': weight,
        'sum_of_digits': st.sidebar.number_input('入院時ADLスコア合計点', min_value=0, step=1),
        'BMI': bmi,
        '入院-手術時間': time_difference,
        '1.04 受傷時年齢': st.sidebar.number_input('受傷時年齢', min_value=0, step=1),
        '2.02 受傷前の活動性': 受傷前の活動性_options[selected_受傷前の活動性],
        '2.03 術前 簡易認知テスト(AMTS)': st.sidebar.number_input('術前簡易認知テスト点数', min_value=0, max_value=10, step=1),
        '2.04 術前全身状態　ASA grade': 術前全身状態_options[selected_術前全身状態],
        '2.07 骨折のタイプ_2. 転位型大腿骨頚部骨折': 骨折のタイプ1_options[selected_骨折のタイプ1],
        '2.07 骨折のタイプ_3. 大腿骨転子部骨折（頚基部骨折を含む）': 骨折のタイプ2_options[selected_骨折のタイプ2],
        '3.03 手術法_4. 髄内釘': 手術法_options[selected_手術法],
        '入院時Alb値': st.sidebar.number_input('入院時Alb値', min_value=0.0, step=0.1),
    }

    return pd.DataFrame(new_data, index=[0])

# Define the main function
def main():
    st.title('大腿骨近位部骨折患者の術後2週時点での歩行自立予測')

    # Get user input
    new_data = get_user_input()

    # Make prediction
    prediction = model.predict(new_data)

    # Display prediction prominently
    st.markdown('## 予測結果')
    if prediction[0] == 0:
        st.success('歩行自立可能')
    elif prediction[0] == 1:
        st.error('歩行自立困難')

    st.markdown('スマートフォンなどでご利用の方は画面左上の横矢印を押すと入力バーが表示されます。')
    st.markdown('ADLスコアに関する詳細は、[こちらのWebサイト](https://drive.google.com/file/d/1AhGz5JY1b8tShiw0wbDIRWQ8R53NNPnh/view?usp=sharing)をご覧ください。')
    st.markdown('術前簡易認知テストに関する詳細は、[こちらのWebサイト](https://drive.google.com/file/d/1q8FgCtwWU8IHpIkNUSejOCQTUscjnSZL/view?usp=sharing)をご覧ください。')
    st.markdown('当Webアプリに関するお問い合わせは、[こちらのWebサイト](https://docs.google.com/forms/d/e/1FAIpQLSd1oTT2XlnQ8R6kGuMBG5jU4ML72Qc5BE4nS3DP5orzY6pt9Q/viewform)からお願いいたします。')

    # Developer introduction
    st.markdown('''### 開発者紹介''')
    st.image('developer_photo.jpg', width=150)
    st.markdown('''
    **秋葉 周**  
    1993年東京生まれ。東京都済生会中央病院リハビリテーション技術科所属。  
    吉備国際大学 通信制大学院保健科学研究科 作業療法学専攻 修士課程在籍中（京極・寺岡ゼミ）。  
    企業や大学教員との共同での臨床研究に精力的に取り組んでいます。
    これまで脳卒中、集中治療、運動器、クリニカルパスなどに関する研究を行ってきました。
    休みの日は野菜を育てたり、料理を作ったりしています。
    ''')

# Run the main function
if __name__ == '__main__':
    main()
