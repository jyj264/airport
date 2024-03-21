# -*- coding:utf-8 -*-
import pandas
import streamlit as st
import time
from enum import Enum

def add_outAirlineA(a, Airline, Flight, Counter, Departure_time, To):
    a = a._append({"Airline": Airline, "Flight": Flight, "To": To, "Counter": Counter, "Departure time": Departure_time,
                  "Remark": "Waiting"}, ignore_index=True)
    return a

def add_outAirlineB(b, Airline, Flight, Counter, Departure_time, To, Gate):
    b = b._append({"Airline": Airline, "Flight": Flight, "To": To, "Departure time": Departure_time, "Gate": Gate,
                  "Remark": "Waiting"}, ignore_index=True)
    return b

def startCheckingA(a, i):
    a["Remark"][i] = "Checking-in"
    return a

def startCheckingB(b, i):
    b["Remark"][i] = "Checking-in"
    return b

def startBoarding(b, i):
    b["Remark"][i] = "Boarding"
    return b

def wait():
    input()

def stopBoardingA(a, i):
    try:
        a = a.drop(i)
    except KeyError:
        pass
    return a

def stopBoardingB(b, i):
    b["Remark"][i] = "Taking off"
    return b

def startBoardingA(a, i):
    a["Remark"][i] = "Boarding"
    return a

def DelayA(a,k,i):
    a["Remark"][i] = "Delayed"
    a["Departure time"][i] = k
    return a

def DelayB(b,k, i):
    b["Remark"][i] = "Delayed"
    b["Departure time"][i] = k
    return b

def CancelA(a,i):
    a["Remark"][i] = "Canceled"
    return a

def CancelB(b,i):
    b["Remark"][i] = "Canceled"
    return b

def EraseA(a, i):
    try:
        a = a.drop(i)
    except KeyError:
        pass
    return a

def EraseB(b, i):
    b = b.drop(i)
    return b

def color_survived(val):
    if val=='Boarding':
        color = 'green'
    if val=='Checking-in':
        color = 'blue'
    if val=='Taking off':
        color = 'black'
    if val=='Canceled':
        color = 'red'
    if val=='Delayed':
        color = 'orange'
    if val=='Waiting':
        color = 'black'
    if val=='Picking up luggage':
        color = 'green'
    return f'color: {color}'

def add_inLine(c, Airline, Flight, Counter, Landing_time, From):
    c = c._append({"Airline": Airline, "Flight": Flight, "From": From, "Counter": Counter, "Landing time": Landing_time,
                  "Remark": "Waiting"}, ignore_index=True)
    return c

def main():
    a = pandas.DataFrame(columns=["Airline", "Flight", "To", "Departure time", "Counter", "Remark"])
    b = pandas.DataFrame(columns=["Airline", "Flight", "To", "Departure time", "Gate", "Remark"])
    c = pandas.DataFrame(columns=["Airline", "Flight","From","Landing time", "Counter", "Remark"])

    st.title("✈ 航班信息管理系统")
    tab1, tab2, tab3, tab4 = st.tabs(["文件", "预览", "添加", "编辑"])

    with tab1:
        st.write("航班信息管理系统 版本：2.0（由Python编写）")
        st.write("图形界面：streamlit")
        st.write("配合显示端screen1.py共同使用")
        try:
            a = pandas.read_csv('Airport_Data_a.csv')
            b = pandas.read_csv('Airport_Data_b.csv')
            c = pandas.read_csv('Airport_Data_c.csv')
        except:
            st.error("源文件不存在或命名错误！")
            st.info("请点击“清空/复位”以创建数据文件")
        k = st.button('清空/复位')
        st.info("航班信息文件(.csv，共3个)存储于airport.py和screen1.py所在的目录下，请勿删除或重命名，否则将会丢失所有数据！")
        if k:
            a = pandas.DataFrame(columns=["Airline", "Flight", "To", "Departure time", "Counter", "Remark"])
            b = pandas.DataFrame(columns=["Airline", "Flight", "To", "Departure time", "Gate", "Remark"])
            c = pandas.DataFrame(columns=["Airline", "Flight", "From", "Landing time", "Counter", "Remark"])
            a.to_csv('Airport_Data_a.csv', index=False)
            b.to_csv('Airport_Data_b.csv', index=False)
            c.to_csv('Airport_Data_c.csv', index=False)
            st.success("操作成功！")
            time.sleep(0.4)
            st.rerun()

    with tab2:
        if st.button('刷新'):
            try:
                a = pandas.read_csv('Airport_Data_a.csv')
                b = pandas.read_csv('Airport_Data_b.csv')
                c = pandas.read_csv('Airport_Data_c.csv')
                st.markdown("值机大厅显示屏预览")
                st.dataframe(a.style.applymap(color_survived, subset=['Remark']))
                st.markdown("候机大厅显示屏预览")
                st.dataframe(b.style.applymap(color_survived, subset=['Remark']))
                st.markdown("行李提取大厅显示屏预览")
                st.dataframe(c.style.applymap(color_survived, subset=['Remark']))
            except FileNotFoundError:
                st.error("源文件不存在或命名错误！")
                st.info("请点击“文件”中的“清空”以创建数据文件")
    with tab3:
        class Mode(str, Enum):
            A, B = '添加出发航班', '添加到达航班'

        tab = st.radio(
            'Mode',
            [mode.value for mode in Mode],
            horizontal=True,
            label_visibility='hidden',
        )
        match tab:
            case Mode.A:
                try:
                    a = pandas.read_csv('Airport_Data_a.csv')
                    b = pandas.read_csv('Airport_Data_b.csv')
                    Airline = st.text_input("Airline:", '')
                    Flight = st.text_input("Flight:", '')
                    Counter = st.text_input("Counter:", '')
                    Departure_time = st.text_input("Departure time:", '')
                    To = st.text_input("To:", '')
                    Gate = st.text_input("Gate:", '')
                    if st.button("保存"):
                        if b["Flight"].isin([Flight]).sum() != 0:
                            st.warning("航班已经存在，不可添加！请您重新输入")
                        else:
                            a = add_outAirlineA(a, Airline, Flight, Counter, Departure_time, To)
                            b = add_outAirlineB(b, Airline, Flight, Counter, Departure_time, To, Gate)
                            st.success("数据保存成功！")

                    a.to_csv('Airport_Data_a.csv', index=False)
                    b.to_csv('Airport_Data_b.csv', index=False)
                except FileNotFoundError:
                    st.error("源文件不存在或命名错误！")
                    st.info("请点击“文件”中的“清空”以创建数据文件")
            case Mode.B:
                try:
                    c = pandas.read_csv('Airport_Data_c.csv')
                    Airline2 = st.text_input("Airline: ", '')
                    Flight2 = st.text_input("Flight: ", '')
                    Counter2 = st.text_input("Counter: ", '')
                    Landing_time2 = st.text_input("Landing time: ", '')
                    From2 = st.text_input("From: ", '')
                    if st.button("保存"):
                        if c["Flight"].isin([Flight2]).sum() != 0:
                            st.warning("航班已经存在，不可添加！请您重新输入")
                        else:
                            c = add_inLine(c, Airline2, Flight2, Counter2, Landing_time2, From2)
                            st.success("数据保存成功！")

                    c.to_csv('Airport_Data_c.csv', index=False)
                except FileNotFoundError:
                    st.error("源文件不存在或命名错误！")
                    st.info("请点击“文件”中的“清空”以创建数据文件")
            case _:
                st.error(f'Unexpected tab: {tab}')
    with (tab4):
        class Mode(str, Enum):
            A, B = '编辑出发航班', '编辑到达航班'

        tab = st.radio(
            'Mode',
            [mode.value for mode in Mode],
            horizontal=True,
            label_visibility='hidden',
        )
        match tab:
            case Mode.A:
                try:
                    a = pandas.read_csv('Airport_Data_a.csv')
                    b = pandas.read_csv('Airport_Data_b.csv')
                    ch2 = st.selectbox("请选择要操作的航班：",
                                     b["Flight"])
                    s = st.selectbox("请选择要进行的操作", ["🔘 广播当前状态","🔵 开始办理值机手续", "🟢 开始登机", "🔴 停止登机", "🟡 航班延误","🟠 航班取消","⚫ 删除航班"])
                    if b["Flight"].isin([ch2]).sum() == 1:
                        rn = b[b['Flight'] == ch2].index[0]
                        if s=='🔵 开始办理值机手续':
                            if st.button("确认",key=324):
                                a = startCheckingA(a, rn)
                                b = startCheckingB(b, rn)
                                st.success("操作成功！")
                        elif s=='🟢 开始登机':
                            if st.button("确认",key=453):
                                b = startBoarding(b, rn)
                                a = startBoardingA(a, rn)
                                st.success("操作成功！")
                        elif s=='🔴 停止登机':
                            if st.button("确认",key=234):
                                a = stopBoardingA(a, rn)
                                b = stopBoardingB(b, rn)
                                st.success("操作成功！")
                        elif s=='🟡 航班延误':
                            k = st.text_input("Departure time:",key=6666)
                            yes=st.button("确认",key=5555)
                            if yes:
                                a = DelayA(a, k, rn)
                                b = DelayB(b, k, rn)
                                st.success("操作成功！")
                        elif s=='🟠 航班取消':
                            if st.button("确认",key=492):
                                a = CancelA(a, rn)
                                b = CancelB(b, rn)
                                st.success("操作成功！")
                        elif s=='⚫ 删除航班':
                            if st.button("确认", key=593):
                                if b["Remark"][rn]!="Taking off":
                                    a = EraseA(a, rn)
                                b = EraseB(b, rn)
                                st.success("操作成功！")
                    try:
                        a.to_csv('Airport_Data_a.csv', index=False)
                        b.to_csv('Airport_Data_b.csv', index=False)
                    except AttributeError:
                        pass
                except FileNotFoundError:
                    st.error("源文件不存在或命名错误！")
                    st.info("请点击“文件”中的“清空”以创建数据文件")
            case Mode.B:
                try:
                    c = pandas.read_csv("Airport_Data_c.csv")
                    ch2 = st.selectbox("请选择要操作的航班：",
                                       c["Flight"])
                    s = st.selectbox("请选择要进行的操作",
                                     ["🟢 开始提取行李","⚫ 删除航班"])
                    if c["Flight"].isin([ch2]).sum() == 1:
                        st.info("请进行操作")
                        rn = c[c['Flight'] == ch2].index[0]
                        if s == '🟢 开始提取行李':
                            if st.button("确认", key=514):
                                c["Remark"][rn] = "Picking up luggage"
                                st.success("操作成功！")
                        elif "⚫ 删除航班":
                            if st.button("确认", key=114):
                                c=c.drop(rn)
                                st.success("操作成功！")
                    try:
                        c.to_csv('Airport_Data_c.csv', index=False)
                    except AttributeError:
                        pass
                except FileNotFoundError:
                    st.error("源文件不存在或命名错误！")
                    st.info("请点击“文件”中的“清空”以创建数据文件")
            case _:
                st.error(f'Unexpected tab: {tab}')


if __name__ == '__main__':
    main()
