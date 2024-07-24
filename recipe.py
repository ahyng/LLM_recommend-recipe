import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import time
import re
from streamlit_modal import Modal
import user_db as db
from llm import llm_recipe


def navigation_button():
    cols = st.columns([3.05, 0.9, 1.15]) 
    
    modal = Modal(
        "내 레시피에 추가", 
        key="My recipes",
        
        # Optional
        padding=20,    # default value
        max_width=550  # default value
    )
    
    with cols[0]:
        if st.button("홈으로 돌아가기"):
            st.session_state.page = 'main'
            st.session_state['response'] = None
            st.rerun()
    with cols[1]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.session_state['response'] = None
            st.rerun()
    with cols[2]:
        open_modal = st.button("내 레시피에 추가")
        if open_modal:
            modal.open()
        if modal.is_open():
            with modal.container():
                st.markdown("**이미 존재하는 레시피 이름입니다.**")
                
                new_food_name = st.text_input("저장을 원하신다면 새 레시피 이름을 적어주세요.", st.session_state.get("food_name", "정보가 없습니다."))
                modal_col_0, modal_col_1  = st.columns([4.3,1]) 
                with modal_col_0:
                    if st.button("이름 변경해서 추가"):
                        # 이름 변경해서 추가 로직
                        st.write("이름 변경해서 추가가 클릭되었습니다.")
                with modal_col_1:
                    if st.button("덮어쓰기"):   
                        # 덮어쓰기 로직
                        st.write("덮어쓰기가 클릭되었습니다.")
            

def recipe_page(index):
    
    cookies = CookieController()
    user_id = cookies.get("user_id")

    # HTML 스타일을 사용한 추가 재료 박스
    def additional_ingredients(ingred, link, img_url, description):
        st.markdown(f"""
                    <div style="padding: 10px; margin-top: 10px; border-bottom: 1px solid #ddd;">
                        <div style="display: flex; align-items: center;">
                            <img src="{img_url}" alt="preview" style="width: 100px; height: 100px; object-fit: cover; margin-right: 10px;">
                            <div>
                                <ul>
                                    <p style="font-weight: 700; font-size: 20px;">{ingred}</p>
                                    <p>{description}</p>
                                    <p><a href="{link}" target="_blank" style="color: gray; font-style: italic;">{ingred} 구매 링크 바로가기</a></p>
                             </ul>
                            </div>
                        </div>
                    </div>  
                    """, unsafe_allow_html=True)
    
    navigation_button()
    
    food_name = st.session_state.get("food_name", "정보가 없습니다.")
    
    if 'response' not in st.session_state:
        st.session_state['response'] = None
        
    if st.session_state['response'] is None:
        response = llm_recipe.GetInformation(food_name)
        st.session_state['response'] = response
    else:
        response = st.session_state['response']
    
    recipe_info = re.sub(r'\[.*\]', '', response)
    st.markdown(f"{recipe_info}")
    
    match = re.search(r'\[.*?\]', response)
    ingredient_list = []
    if match:
        ingredient_list = match.group()
        ingredient_list = ingredient_list.strip('[]').replace('"', '').split(', ')
    
    st.header('추가구매 추천 재료')
    
    # if ingredient_list:
    need_ingredient = set(ingredient_list)
    # else:
    #     need_ingredient = set([])
        
    have_ingredient = set(db.get_ingredient(user_id))
    add_ingredient = need_ingredient - have_ingredient
    
    if add_ingredient:
        for ingred in list(add_ingredient):
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"  # 예시 이미지 URL을 적절히 변경
            description = "마켓 컬리에서 찾은 관련 상품입니다."
            additional_ingredients(ingred, purchase_link, img_url, description)