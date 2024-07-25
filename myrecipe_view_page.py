import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import re

import user_db as db

def navigation_button(id, food):
    cols = st.columns([5, 2, 1]) 
    with cols[1]:
        if st.button("목록으로 돌아가기"):
            st.session_state.page = 'myrecipe_list'
            st.rerun()
    with cols[2]:
        if st.button("삭제"):
            db.remove_recipe(id, food)
            st.session_state.page = 'myrecipe_list'
            st.rerun()

def display_my_recipe_view():
    cookies = CookieController()
    user_id = cookies.get("user_id")
    food = st.session_state.get("my_food_name")
    navigation_button(user_id, food)

     # HTML 스타일을 사용한 추가 재료 박스
    def additional_ingredients(ingred, link):
        st.markdown(f"""
                <div style="padding: 5px; margin-top: 5px">
                    <ul style="list-style-type: disc; margin: 0; padding-left: 20px; align-items: center;">
                        <li>
                            <a href="{link}" 
                                    style="color: black; 
                                    text-decoration: none;
                                    font-size: 20px; 
                                    font-weight: bold;">
                                {ingred}
                            </a>
                        </li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    recipe = db.get_recipe(user_id, food)

    
    recipe_info = re.sub(r'\[.*\]', '', recipe)
    st.markdown(f"{recipe_info}")

    match = re.search(r'\[.*?\]', recipe)
    if match:
        ingredient_list = match.group()
        ingredient_list = ingredient_list.strip('[]').replace('"', '').split(', ')
    
    st.header('추가구매 추천 재료')

    if ingredient_list:
        need_ingredient = set(ingredient_list)
    else:
        need_ingredient = set([])
    have_ingredient = set(db.get_ingredient(user_id))

    #내가 가진 재료 외 필요한 재료 구하기
    add_ingredient = need_ingredient - have_ingredient
    
    if add_ingredient:
        #마켓컬리 로고사진과 문구 출력
        img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"
        st.markdown(f"""
            <div style="padding: 10px; margin-top: 10px; border-bottom: 1px solid #ddd;">
                <div style="display: flex; flex-direction: column;">
                    <img src="{img_url}" alt="preview" style="width: 100px; height: 100px; object-fit: cover; margin-bottom: 10px;">
                </div>
                <div style="text-align: left; font-size: 18px; padding: 1px;">
                    <span>{"상품명을 누르시면 마켓컬리 구매 링크로 연결됩니다."}</span>
                </div>
            </div>  
            """, unsafe_allow_html=True)
        
        for ingred in list(add_ingredient):
            #추가 재료 품목을 링크로 출력
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            additional_ingredients(ingred, purchase_link)
            