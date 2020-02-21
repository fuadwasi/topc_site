from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login  as auth_login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
import string

from django.utils import timezone
from datetime import datetime
from django.db.models.functions import Now

from TOPC_Reg_SYS.models import ALLStudents, RegStudents
from . import email_conf_send
from django.conf import settings


def dashboard(request):
    if request.user.is_authenticated:
        all_campus = RegStudents.objects.all()
        total_std_count = ALLStudents.objects.all().count()
        total_reg_count = RegStudents.objects.all().count()
        seat_available = settings.SEAT_COUNT - total_reg_count
        main_campus = len(RegStudents.objects.filter(basic_info__campus='MC'))
        uttara_campus = len(RegStudents.objects.filter(basic_info__campus='UC'))
        male = len(RegStudents.objects.filter(basic_info__gender__exact='Male'))
        female = len(RegStudents.objects.filter(basic_info__gender__exact='Female'))
        day = len(RegStudents.objects.filter(basic_info__shift__exact='Day'))
        evening = len(RegStudents.objects.filter(basic_info__shift__exact='Evening'))
        m_size = len(RegStudents.objects.filter(t_shirt__exact='M'))
        l_size = len(RegStudents.objects.filter(t_shirt__exact='L'))
        xl_size = len(RegStudents.objects.filter(t_shirt__exact='XL'))
        xxl_size = len(RegStudents.objects.filter(t_shirt__exact='XXL'))
        xxxl_size = len(RegStudents.objects.filter(t_shirt__exact='XXXL'))
        cse = len(RegStudents.objects.filter(basic_info__department__exact="CSE"))
        swe = len(RegStudents.objects.filter(basic_info__department__exact="SWE"))
        cis = len(RegStudents.objects.filter(basic_info__department__exact="CIS"))
        other_dept = total_reg_count - cse - cis - swe

        # # ........................ For 1st sem MC Day.......................................
        #     A_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="A") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     B_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="B") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     C_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="C") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     D_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="D") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     E_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="E") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     F_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="F") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     G_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="G") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     H_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="H") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     I_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="I") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     J_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="J") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     K_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="K") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     L_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="L") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     M_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="M") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     N_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="N") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     O_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="O") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     P_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="P") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     Q_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="Q") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     UC_A_1st = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="UC-A") & Q(basic_info__campus__exact="UC") & Q(
        #             basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day")))
        #     Eve_A_1st = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="Eve-A") & Q(basic_info__campus__exact="MC") & Q(
        #             basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Evening")))
        #     Eve_B_1st = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="Eve-B") & Q(basic_info__campus__exact="MC") & Q(
        #             basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Evening")))
        #
        #
        # #  .................... 2nd Semester .................................... #
        #     A_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="A") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     B_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="B") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     C_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="C") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     D_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="D") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     E_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="E") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     F_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="F") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     G_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="G") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     H_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="H") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     I_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="I") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     J_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="J") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     K_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="K") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     L_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="L") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     M_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="M") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     N_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="N") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     O_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="O") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     P_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="P") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     Q_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="Q") & Q(basic_info__campus__exact="MC") & Q(
        #         basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     UC_A_2nd = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="UC-A") & Q(basic_info__campus__exact="UC") & Q(
        #             basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day")))
        #     Eve_A_2nd = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="Eve-A") & Q(basic_info__campus__exact="MC") & Q(
        #             basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Evening")))
        #     Eve_B_2nd = len(RegStudents.objects.filter(
        #         Q(basic_info__section__exact="Eve-B") & Q(basic_info__campus__exact="MC") & Q(
        #             basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Evening")))
        # ........................ For 1st sem MC Day.......................................
        A_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="A") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        B_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="B") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        C_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="C") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        D_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="D") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        E_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="E") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        F_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="F") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        G_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="G") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        H_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="H") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        I_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="I") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        J_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="J") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        K_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="K") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        L_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="L") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        M_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="M") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        N_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="N") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        O_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="O") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        P_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="P") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        Q_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="Q") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        UC_A_1st = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="UC-A") & Q(basic_info__campus__exact="UC") & Q(
                basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Day") & Q(
                basic_info__department__exact='CSE')))
        Eve_A_1st = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="Eve-A") & Q(basic_info__campus__exact="MC") & Q(
                basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Evening") & Q(
                basic_info__department__exact='CSE')))
        Eve_B_1st = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="Eve-B") & Q(basic_info__campus__exact="MC") & Q(
                basic_info__semester__exact="1st") & Q(basic_info__shift__exact="Evening") & Q(
                basic_info__department__exact='CSE')))

        #  .................... 2nd Semester .................................... #
        A_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="A") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        B_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="B") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        C_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="C") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        D_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="D") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        E_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="E") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        F_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="F") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        G_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="G") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        H_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="H") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        I_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="I") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        J_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="J") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        K_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="K") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        L_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="L") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        M_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="M") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        N_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="N") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        O_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="O") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        P_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="P") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        Q_2nd = len(RegStudents.objects.filter(Q(basic_info__section__exact="Q") & Q(basic_info__campus__exact="MC") & Q(
            basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
            basic_info__department__exact='CSE')))
        UC_A_2nd = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="UC-A") & Q(basic_info__campus__exact="UC") & Q(
                basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Day") & Q(
                basic_info__department__exact='CSE')))
        Eve_A_2nd = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="Eve-A") & Q(basic_info__campus__exact="MC") & Q(
                basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Evening") & Q(
                basic_info__department__exact='CSE')))
        Eve_B_2nd = len(RegStudents.objects.filter(
            Q(basic_info__section__exact="Eve-B") & Q(basic_info__campus__exact="MC") & Q(
                basic_info__semester__exact="2nd") & Q(basic_info__shift__exact="Evening") & Q(
                basic_info__department__exact='CSE')))

        contex = {'total_std_count': total_std_count,
                  'total_reg_count': total_reg_count,
                  'seat_available': seat_available,
                  'main_campus': main_campus, 'uttara_camp': uttara_campus,
                  'male': male, 'female': female,
                  'day': day, 'evening': evening,
                  'm_size': m_size,
                  'l_size': l_size,
                  'xl_size': xl_size,
                  'xxl_size': xxl_size,
                  'xxxl_size': xxxl_size,
                  'cse': cse,
                  'swe': swe,
                  'cis': cis,
                  'other_dept': other_dept,
                  'A_1st': A_1st,
                  'B_1st': B_1st,
                  'C_1st': C_1st,
                  'D_1st': D_1st,
                  'E_1st': E_1st,
                  'F_1st': F_1st,
                  'G_1st': G_1st,
                  'H_1st': H_1st,
                  'I_1st': I_1st,
                  'J_1st': J_1st,
                  'K_1st': K_1st,
                  'L_1st': L_1st,
                  'M_1st': M_1st,
                  'N_1st': N_1st,
                  'O_1st': O_1st,
                  'P_1st': P_1st,
                  'Q_1st': Q_1st,

                  # 2nd
                  'A_2nd': A_2nd,
                  'B_2nd': B_2nd,
                  'C_2nd': C_2nd,
                  'D_2nd': D_2nd,
                  'E_2nd': E_2nd,
                  'F_2nd': F_2nd,
                  'G_2nd': G_2nd,
                  'H_2nd': H_2nd,
                  'I_2nd': I_2nd,
                  'J_2nd': J_2nd,
                  'K_2nd': K_2nd,
                  'L_2nd': L_2nd,
                  'M_2nd': M_2nd,
                  'N_2nd': N_2nd,
                  'O_2nd': O_2nd,
                  'P_2nd': P_2nd,
                  'Q_2nd': Q_2nd,

                  # UC
                  'UC_A_1st': UC_A_1st,
                  'UC_A_2nd': UC_A_2nd,
                  # Evening
                  'Eve_A_1st': Eve_A_1st,
                  'Eve_B_1st': Eve_B_1st,
                  'Eve_A_2nd': Eve_A_2nd,
                  'Eve_B_2nd': Eve_B_2nd,

                  }

        # return HttpResponse(str(len(main_camp)))
        return render(request, 'dashboard.html', contex)
    else:
        return redirect('home')
