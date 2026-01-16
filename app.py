import streamlit as st
import json
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="프로젝트 투표",
    page_icon="🏆",
    layout="wide"
)

# 데이터 파일
VOTE_FILE = "votes.json"

# 팀 정보
teams_data = [
    {"id": "1팀", "name": "인계템", "desc": "사람별 연락주기 관리 시스템", "emoji": "📊"},
    {"id": "2팀", "name": "소마고 상식 퀴즈", "desc": "소마고 상식퀴즈", "emoji": "🧠"},
    {"id": "3팀", "name": "개인 지출 관리 프로그램", "desc": "지출관리", "emoji": "✅"},
    {"id": "4팀", "name": "무비픽", "desc": "부마민국 영화추천", "emoji": "🎬"},
    {"id": "5팀", "name": "미니게임", "desc": "3가지 미니게임", "emoji": "🎮"},
    {"id": "6팀", "name": "Today Fortune", "desc": "오늘의 운세", "emoji": "🔮"},
    {"id": "7팀", "name": "해주세요", "desc": "해주세요/도와줄게요", "emoji": "🙋🏻"},
    {"id": "8팀", "name": "거북이의 여행", "desc": "도박 베팅은 몸에 안좋아요", "emoji": "🐢"},
    {"id": "9팀", "name": "급식알리미", "desc": "급식메뉴검색", "emoji": "🍽️"},
    {"id": "10팀", "name": "3분 MBTI", "desc": "성격 유형 분석", "emoji": "🧠"},
]

# 함수들
def load_votes():
    if os.path.exists(VOTE_FILE):
        try:
            with open(VOTE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_vote(voter, teams):
    votes = load_votes()
    votes[voter] = {
        'teams': teams,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(VOTE_FILE, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)

def get_results():
    votes = load_votes()
    results = {team['id']: 0 for team in teams_data}
    
    for vote_data in votes.values():
        voted_teams = vote_data.get('teams', [])
        for team in voted_teams:
            if team in results:
                results[team] += 1
    
    return results

# 세션 상태 초기화
if 'selected_teams' not in st.session_state:
    st.session_state.selected_teams = []

# 메인 UI
st.title("🏆 2026 파이썬 미니 프로젝트 투표")
st.markdown("### 가장 우수하다고 생각하는 프로젝트 **2개**에 투표해주세요!")
st.markdown("---")

# 탭 생성
tab1, tab2 = st.tabs(["📝 투표하기", "📊 결과 보기"])

# 투표하기 탭
with tab1:
    voter_name = st.text_input(
        "👤 이름을 입력하세요",
        placeholder="홍길동",
        key="voter_input"
    )
    
    if voter_name:
        votes = load_votes()
        
        if voter_name in votes:
            st.warning(f"⚠️ {voter_name}님은 이미 투표하셨습니다!")
            voted_teams = votes[voter_name].get('teams', [])
            st.info(f"**투표한 팀**: {', '.join(voted_teams)}")
            st.caption(f"투표 시각: {votes[voter_name]['timestamp']}")
            
            if st.button("투표 수정하기 (재투표)"):
                votes.pop(voter_name)
                with open(VOTE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(votes, f, ensure_ascii=False, indent=2)
                st.session_state.selected_teams = []
                st.success("투표가 취소되었습니다. 다시 투표해주세요!")
                st.rerun()
        
        else:
            st.markdown("---")
            
            # 선택 현황 표시
            selected_count = len(st.session_state.selected_teams)
            
            if selected_count == 0:
                st.subheader("🥇 1번째 팀을 선택하세요")
                st.caption("💡 카드를 클릭하면 선택됩니다!")
            elif selected_count == 1:
                st.subheader("🥈 2번째 팀을 선택하세요")
                st.info(f"✅ 1번째 선택: **{st.session_state.selected_teams[0]}**")
            else:
                st.success("✅ 2개 팀 선택 완료!")
                st.info(f"**선택한 팀**: {', '.join(st.session_state.selected_teams)}")
            
            st.markdown("---")
            
            # 팀 카드
            for i in range(0, len(teams_data), 2):
                cols = st.columns(2)
                
                for j in range(2):
                    if i + j < len(teams_data):
                        team = teams_data[i + j]
                        
                        with cols[j]:
                            is_selected = team['id'] in st.session_state.selected_teams
                            
                            # 컨테이너로 카드 만들기 (HTML 대신)
                            if is_selected:
                                # 선택된 카드
                                st.markdown(
                                    f"""
                                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                padding: 30px; 
                                                border-radius: 15px; 
                                                border: 3px solid #667eea;
                                                text-align: center;
                                                margin-bottom: 15px;">
                                        <div style="font-size: 64px; margin-bottom: 10px;">{team['emoji']}</div>
                                        <div style="font-size: 24px; font-weight: bold; color: white; margin-bottom: 8px;">{team['id']} ✓</div>
                                        <div style="font-size: 18px; font-weight: 600; color: white; margin-bottom: 5px;">{team['name']}</div>
                                        <div style="font-size: 14px; color: rgba(255,255,255,0.9);">{team['desc']}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            else:
                                # 선택 안 된 카드
                                st.markdown(
                                    f"""
                                    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.13) 0%, rgba(118,75,162,0.13) 100%); 
                                                padding: 30px; 
                                                border-radius: 15px; 
                                                border: 2px solid #e0e0e0;
                                                text-align: center;
                                                margin-bottom: 15px;">
                                        <div style="font-size: 64px; margin-bottom: 10px;">{team['emoji']}</div>
                                        <div style="font-size: 24px; font-weight: bold; color: #667eea; margin-bottom: 8px;">{team['id']}</div>
                                        <div style="font-size: 18px; font-weight: 600; color: #333; margin-bottom: 5px;">{team['name']}</div>
                                        <div style="font-size: 14px; color: #666;">{team['desc']}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            
                            # 버튼
                            if is_selected:
                                if st.button(
                                    f"✗ 선택 취소",
                                    key=f"cancel_{team['id']}",
                                    use_container_width=True
                                ):
                                    st.session_state.selected_teams.remove(team['id'])
                                    st.rerun()
                            else:
                                button_disabled = len(st.session_state.selected_teams) >= 2
                                
                                if st.button(
                                    f"✓ 선택",
                                    key=f"select_{team['id']}",
                                    type="primary" if not button_disabled else "secondary",
                                    use_container_width=True,
                                    disabled=button_disabled
                                ):
                                    if len(st.session_state.selected_teams) < 2:
                                        st.session_state.selected_teams.append(team['id'])
                                        st.rerun()
            
            # 투표 확정 버튼
            if len(st.session_state.selected_teams) == 2:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    if st.button("🗳️ 투표 확정", type="primary", use_container_width=True):
                        save_vote(voter_name, st.session_state.selected_teams)
                        st.success(f"✅ {voter_name}님, 투표 완료!")
                        st.balloons()
                        st.session_state.selected_teams = []
                        st.rerun()


with tab2:
    st.header("📊 실시간 투표 결과")
    
    # 관리자 비밀번호 입력
    result_password = st.text_input(
        "🔐 관리자 비밀번호를 입력하세요",
        type="password",
        key="result_password"
    )
    
    if result_password == "admin1234":  # 사이드바와 같은 비밀번호
        st.success("✅ 관리자 인증 완료")
        st.markdown("---")
        
        results = get_results()
        votes = load_votes()
        total_votes = len(votes)
        total_vote_count = sum(results.values())
        
        # 통계
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("투표 참여", f"{total_votes}명")
        with col2:
            st.metric("총 득표", f"{total_vote_count}표")
        with col3:
            st.metric("투표율", f"{(total_votes/40)*100:.0f}%")
        
        st.markdown("---")
        
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (team_id, count) in enumerate(sorted_results, 1):
            team_info = next((t for t in teams_data if t['id'] == team_id), None)
            
            if team_info:
                percentage = (count / total_vote_count * 100) if total_vote_count > 0 else 0
                
                medal = ""
                if rank == 1:
                    medal = "🥇"
                elif rank == 2:
                    medal = "🥈"
                elif rank == 3:
                    medal = "🥉"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(
                        f"""
                        <div style="padding: 15px; border-radius: 10px; background: white; border-left: 5px solid #667eea; margin-bottom: 10px;">
                            <span style="font-size: 24px;">{medal}</span>
                            <span style="font-size: 20px; font-weight: bold;"> {rank}위. {team_info['emoji']} {team_id}</span>
                            <br>
                            <span style="color: #666; font-size: 14px;">{team_info['name']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.metric("득표", f"{count}표")
                
                st.progress(percentage / 100 if total_vote_count > 0 else 0)
                st.caption(f"{percentage:.1f}%")
                st.markdown("")
    
    elif result_password:
        st.error("❌ 비밀번호가 틀렸습니다!")
    else:
        st.info("💡 투표 결과는 관리자만 확인할 수 있습니다.")


# 사이드바
st.sidebar.title("⚙️ 관리자")
admin_password = st.sidebar.text_input("관리자 비밀번호", type="password")

if admin_password == "admin1234":
    st.sidebar.success("✅ 관리자 로그인")
    
    votes = load_votes()
    st.sidebar.metric("현재 투표자", f"{len(votes)}명")
    st.sidebar.metric("총 득표", f"{sum(get_results().values())}표")
    
    if st.sidebar.button("🔄 투표 전체 초기화", type="primary"):
        if os.path.exists(VOTE_FILE):
            os.remove(VOTE_FILE)
        st.sidebar.success("투표가 초기화되었습니다!")
        st.rerun()
    
    if st.sidebar.checkbox("투표자 명단 보기"):
        st.sidebar.markdown("---")
        for voter, data in votes.items():
            teams = data.get('teams', [])
            st.sidebar.text(f"{voter} → {', '.join(teams)}")
    
    if votes:
        st.sidebar.download_button(
            "📥 투표 데이터 다운로드",
            json.dumps(votes, ensure_ascii=False, indent=2),
            "votes.json",
            "application/json"
        )
