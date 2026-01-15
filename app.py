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

# 팀 정보 (실제 팀 정보로 수정하세요!)
teams_data = [
    {"id": "1팀", "name": "학급 성적 관리", "desc": "성적 입력 및 통계 분석", "emoji": "📊"},
    {"id": "2팀", "name": "급식 메뉴 추천기", "desc": "랜덤 메뉴 추천 및 투표", "emoji": "🍽️"},
    {"id": "3팀", "name": "출석 체크 시스템", "desc": "지각 관리 및 출석률", "emoji": "✅"},
    {"id": "4팀", "name": "용돈 관리 프로그램", "desc": "수입/지출 기록", "emoji": "💰"},
    {"id": "5팀", "name": "To-do 관리", "desc": "할 일 우선순위 관리", "emoji": "📝"},
    {"id": "6팀", "name": "숫자 맞추기 게임", "desc": "UP/DOWN 게임", "emoji": "🎮"},
    {"id": "7팀", "name": "공부 시간 기록", "desc": "과목별 시간 추적", "emoji": "⏰"},
    {"id": "8팀", "name": "시험 점수 계산기", "desc": "등급 자동 계산", "emoji": "📈"},
    {"id": "9팀", "name": "MBTI 테스트", "desc": "성격 유형 분석", "emoji": "🧠"},
    {"id": "10팀", "name": "텍스트 RPG", "desc": "선택형 게임", "emoji": "⚔️"},
]

# 함수들
def load_votes():
    """저장된 투표 불러오기"""
    if os.path.exists(VOTE_FILE):
        try:
            with open(VOTE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_vote(voter, team):
    """투표 저장하기"""
    votes = load_votes()
    votes[voter] = {
        'team': team,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(VOTE_FILE, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)

def get_results():
    """투표 결과 집계"""
    votes = load_votes()
    results = {team['id']: 0 for team in teams_data}
    
    for vote_data in votes.values():
        team = vote_data['team']
        if team in results:
            results[team] += 1
    
    return results

# 메인 UI
st.title("🏆 2026 파이썬 미니 프로젝트 투표")
st.markdown("### 가장 우수하다고 생각하는 프로젝트에 투표해주세요!")
st.markdown("---")

# 탭 생성
tab1, tab2 = st.tabs(["📝 투표하기", "📊 결과 보기"])

# 투표하기 탭
with tab1:
    # 이름 입력
    voter_name = st.text_input(
        "👤 이름을 입력하세요",
        placeholder="홍길동",
        key="voter_input"
    )
    
    if voter_name:
        votes = load_votes()
        
        # 이미 투표했는지 확인
        if voter_name in votes:
            st.warning(f"⚠️ {voter_name}님은 이미 투표하셨습니다!")
            st.info(f"**투표한 팀**: {votes[voter_name]['team']}")
            st.caption(f"투표 시각: {votes[voter_name]['timestamp']}")
            
            # 투표 수정 옵션
            if st.button("투표 수정하기 (재투표)"):
                votes.pop(voter_name)
                with open(VOTE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(votes, f, ensure_ascii=False, indent=2)
                st.success("투표가 취소되었습니다. 다시 투표해주세요!")
                st.rerun()
        
        else:
            st.markdown("---")
            st.subheader("투표할 팀을 선택하세요")
            st.caption("💡 카드를 클릭하면 바로 투표가 완료됩니다!")
            
            # 팀 카드 (2열 배치)
            for i in range(0, len(teams_data), 2):
                cols = st.columns(2)
                
                for j in range(2):
                    if i + j < len(teams_data):
                        team = teams_data[i + j]
                        
                        with cols[j]:
                            # 카드 디자인
                            st.markdown(f"""
                                <div style='
                                    padding: 30px;
                                    border-radius: 15px;
                                    background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
                                    border: 2px solid #e0e0e0;
                                    text-align: center;
                                    margin-bottom: 20px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                '>
                                    <div style='font-size: 64px; margin-bottom: 15px;'>{team['emoji']}</div>
                                    <div style='font-size: 24px; font-weight: bold; color: #667eea; margin-bottom: 10px;'>
                                        {team['id']}
                                    </div>
                                    <div style='font-size: 18px; font-weight: 600; color: #333; margin-bottom: 8px;'>
                                        {team['name']}
                                    </div>
                                    <div style='font-size: 14px; color: #666;'>
                                        {team['desc']}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # 투표 버튼
                            if st.button(
                                f"✓ 이 팀에 투표",
                                key=f"vote_{team['id']}",
                                type="primary",
                                use_container_width=True
                            ):
                                save_vote(voter_name, team['id'])
                                st.success(f"✅ {voter_name}님, {team['id']}에 투표 완료!")
                                st.balloons()
                                st.rerun()

# 결과 보기 탭
with tab2:
    st.header("📊 실시간 투표 결과")
    
    results = get_results()
    votes = load_votes()
    total_votes = len(votes)
    
    # 통계
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 투표 수", f"{total_votes}표")
    with col2:
        st.metric("참여 팀", f"{len(teams_data)}팀")
    with col3:
        st.metric("투표율", f"{(total_votes/40)*100:.0f}%" if total_votes > 0 else "0%")
    
    st.markdown("---")
    
    # 결과 정렬
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    # 순위 표시
    for rank, (team_id, count) in enumerate(sorted_results, 1):
        # 팀 정보 찾기
        team_info = next((t for t in teams_data if t['id'] == team_id), None)
        
        if team_info:
            percentage = (count / total_votes * 100) if total_votes > 0 else 0
            
            # 메달
            medal = ""
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            
            # 결과 카드
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background: white;
                        border-left: 5px solid #667eea;
                        margin-bottom: 10px;
                    '>
                        <span style='font-size: 24px;'>{medal}</span>
                        <span style='font-size: 20px; font-weight: bold;'> {rank}위. {team_info['emoji']} {team_id}</span>
                        <br>
                        <span style='color: #666; font-size: 14px;'>{team_info['name']}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("득표", f"{count}표")
            
            # 프로그레스 바
            st.progress(percentage / 100 if total_votes > 0 else 0)
            st.caption(f"{percentage:.1f}%")
            st.markdown("")

# 사이드바 - 관리자 기능
st.sidebar.title("⚙️ 관리자")
admin_password = st.sidebar.text_input("관리자 비밀번호", type="password")

if admin_password == "admin1234":  # 비밀번호 변경하세요!
    st.sidebar.success("✅ 관리자 로그인")
    
    votes = load_votes()
    st.sidebar.metric("현재 투표 수", len(votes))
    
    # 초기화 버튼
    if st.sidebar.button("🔄 투표 전체 초기화", type="primary"):
        if os.path.exists(VOTE_FILE):
            os.remove(VOTE_FILE)
        st.sidebar.success("투표가 초기화되었습니다!")
        st.rerun()
    
    # 투표자 목록
    if st.sidebar.checkbox("투표자 명단 보기"):
        st.sidebar.markdown("---")
        for voter, data in votes.items():
            st.sidebar.text(f"{voter} → {data['team']}")
    
    # 데이터 다운로드
    if votes:
        st.sidebar.download_button(
            "📥 투표 데이터 다운로드",
            json.dumps(votes, ensure_ascii=False, indent=2),
            "votes.json",
            "application/json"
        )