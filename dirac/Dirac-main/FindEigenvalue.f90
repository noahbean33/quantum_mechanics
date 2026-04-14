program FindEigenvalue

  use shared
  use funcs

  implicit none

  !! Define Quantities: !!

  !! CODATA(98)

  real(dp) :: box_size, radius

  real(dp) :: eigenvalue(num_states), test_eigenvalue
  real(dp) :: error_est(num_states)
  integer  :: nodes(num_states)
  integer  :: current_sign, new_sign

  integer  :: r_it, attempt, guess ! iterators

  real(dp) :: scalefactor, sum_integral, Fdiff, deltaEV
  real(dp) :: Fdiff_up, Fdiff_down, Fderiv
  real(dp) :: exact_solution(3)

  real(dp), dimension(3), parameter :: n_state = (/ 1, 2, 2 /)

  integer :: accept_ev

  real(dp) :: proportional_factor, EVshift

  integer, parameter :: solving_method = 1 ! Runge Kutta
!!$  integer, parameter :: solving_method = 2 ! Adams Bashforth

  allocate(F_state(n_steps,num_states))
  allocate(G_state(n_steps,num_states))

  proportional_factor = h_step

  !! Coulomb potential:

!!$  open(21,file="coulomb.dat",status="unknown")
!!$  do r_it = 1, n_steps
!!$     write(21,'(3F20.14)')r_it*h_step,Coulomb(r_it*h_step),-alpha/(r_it*h_step)
!!$  end do
!!$  close(21)

  !! Solver: !!
  !! Iteratively solve Dirac equation to find E_e = E - m

  box_size = h_step*n_steps

  exact_solution(1) = m_reduced*(sqrt(1.0_dp-(alpha**2))) - m_reduced  ! E - m
  exact_solution(2) = m_reduced*(sqrt((1.0_dp+sqrt(1.0_dp-(alpha**2)))/2.0_dp)) - m_reduced  ! E - m
!  exact_solution(3) = m_reduced*(sqrt((1.0_dp+sqrt(1.0_dp-(alpha**2)))/2.0_dp)) - m_reduced  ! E - m
  exact_solution(3) = m_reduced*sqrt((1.0_dp+(alpha/(n_state(1)-1.0_dp+sqrt(1.0_dp-(alpha**2))))**2)**(-1)) - m_reduced
!!$  exact_solution(:) = m_reduced*(1.0_dp-((alpha**2)/(2.0_dp*(n_state(:)**2)))*(1.0_dp+((alpha**2)/n_state(:))*(0.5_dp-(3.0_dp/(4.0_dp*n_state(:)))))) - m_reduced  ! E - m
  do state = 1, 3
     write(*,'(A,I1,A,F13.7,A,F18.12,A)')"state ",state," exact = ",exact_solution(state)," = ",exact_solution(state)*fermi*1000," keV"
  end do

  eigenvalue(:)   = (1.0_dp-proportional_factor)*exact_solution(:) !+ m_reduced  ! initial guess = 2.7 keV
  F_state(:,:)    = 0.0_dp
  G_state(:,:)    = 0.0_dp

  if ( solving_method == 1 ) print *,"USING RUNGE KUTTA TO FIND EIGENVALUE"
  if ( solving_method == 2 ) print *,"USING ADAMS BASHFORTH TO FIND EIGENVALUE"

  do state = 1, 1!num_states

     do attempt = 1, max_attempts

        write(*,'(a,F18.12,a)')"eigenvalue = ",eigenvalue(state)*fermi*1000," keV"
        write(*,'(a,F18.12,a)')"exact soln = ",exact_solution(state)*fermi*1000," keV"
        ! calculate F and G
        test_eigenvalue = eigenvalue(state)
        if ( solving_method == 1 ) then
           call Runge_up(test_eigenvalue)
           call Runge_down(test_eigenvalue)
        else if ( solving_method == 2 ) then
           call FGIntegral(test_eigenvalue)
        end if
        ! scale the solutions to make the 
        ! match point smooth
        scalefactor = G_state(match+1,state)/G_state(match,state)
        G_state(:match,state) = G_state(:match,state)*scalefactor
        F_state(:match,state) = F_state(:match,state)*scalefactor
        ! calculate integral |F|^2 + |G|^2 (extended Simpson's Rule)
        sum_integral = 0.0_dp
        sum_integral = sum_integral + h_step*(abs(F_state(1,state))**2 + abs(G_state(1,state))**2)
        sum_integral = sum_integral + h_step*(abs(F_state(n_steps,state))**2 + abs(G_state(n_steps,state))**2)
        do r_it = 2, n_steps-2, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 2.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        do r_it = 3, n_steps-1, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 4.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        sum_integral = sum_integral/3.0_dp
        ! normalize
        F_state(:,state) = F_state(:,state)/sqrt(abs(sum_integral))
        G_state(:,state) = G_state(:,state)/sqrt(abs(sum_integral))
        ! calculate discontinuity
        Fdiff = (F_state(match+1,state) - F_state(match,state))/F_state(match,state)
!!$           print *,"fdiff = ",Fdiff 

!!$           !! !!!!!!!!!!!!!!!!
!!$           ! check:
!!$           sum_integral = 0.0_dp
!!$           do r_it = 1, n_steps
!!$              sum_integral = sum_integral + h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
!!$           end do
!!$           !
!!$           write(*,*)" CHECKING: SUM = ",sum_integral
!!$           ! check better:
!!$           sum_integral = 0.0_dp
!!$           sum_integral = sum_integral + h_step*(abs(F_state(1,state))**2 + abs(G_state(1,state))**2)
!!$           sum_integral = sum_integral + h_step*(abs(F_state(n_steps,state))**2 + abs(G_state(n_steps,state))**2)
!!$           do r_it = 2, n_steps-2, 2
!!$              !
!!$              radius = r_it*h_step
!!$              sum_integral = sum_integral &
!!$                   & + 2.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
!!$              !
!!$           end do
!!$           do r_it = 3, n_steps-1, 2
!!$              !
!!$              radius = r_it*h_step
!!$              sum_integral = sum_integral &
!!$                   & + 4.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
!!$              !
!!$           end do
!!$           sum_integral = sum_integral/3.0_dp
!!$           !
!!$           write(*,*)" CHECKING BETTER: SUM = ",sum_integral
!!$           !! !!!!!!!!!!!!!!!!

!!$           Fderiv = (Fdiff_up-Fdiff_down)/proportional_factor
!!$           print *,"Fderiv = ",Fderiv

        !           if ( ( abs(Fdiff_down) < abs(Fdiff) ) .or. ( abs(Fdiff_up) < abs(Fdiff) ) ) then
!!$              EVshift = Fdiff/Fderiv
!!$              print *,"EVshift = ",EVshift," = ",100.0_dp*EVshift/eigenvalue(state),"%"
!!$              eigenvalue(state) = eigenvalue(state) - EVshift
        !
!!$              if ( abs(Fdiff_up) .le. abs(Fdiff_down) ) then
!!$                 eigenvalue(state) = (1.0_dp+proportional_factor)*eigenvalue(state)
!!$              end if
!!$              if ( abs(Fdiff_down) .le. abs(Fdiff_up) ) then
!!$                 eigenvalue(state) = (1.0_dp-proportional_factor)*eigenvalue(state)
!!$              end if
        EVshift = -G_state(match,state)*Fdiff*F_state(match,state)
        print *,"EV shift = ",EVshift*fermi*1000," keV"

        if ( abs(EVshift) < yErrReq ) then
           print *,"EV shift is small enough now... done."
           write(*,'(a,e12.6,a,e12.6)')"EVshift = ",abs(Evshift)," vs yErrReq = ",yErrReq
           go to 53
        end if

        eigenvalue(state) = eigenvalue(state) + EVshift
        !           else
!!$              if ( abs(Fdiff_up) < abs(Fdiff) ) then
!!$                 eigenvalue(state) = (1.0_dp+proportional_factor)*eigenvalue(state)
!!$              end if
!!$              if ( abs(Fdiff_down) < abs(Fdiff) ) then
!!$                 eigenvalue(state) = (1.0_dp-proportional_factor)*eigenvalue(state)
!!$              end if
        !              if ( ( abs(Fdiff_down) > abs(Fdiff) ) .and. ( abs(Fdiff_up) > abs(Fdiff) ) ) then
        ! "Solution is in a minimum"
        !                 proportional_factor = 0.5_dp*proportional_factor
        !              end if
        !           end if

        open(61,file='Wavefunctions.dat',status='unknown')
        do r_it = 1, n_steps,1000
           write(61,*)r_it*h_step,F_state(r_it,state),G_state(r_it,state)
        end do
        close(61)
        !
        if ( attempt == max_attempts ) STOP ' too many attempts '
        !
     end do
     !


53   continue

     do guess = 1, 200

        write(*,'(a,F18.12,a)')"eigenvalue = ",eigenvalue(state)*fermi*1000.0_dp," keV"
        write(*,'(a,F18.12,a)')"exact soln = ",exact_solution(state)*fermi*1000.0_dp," keV"

        F_state(:,state) = 0.0_dp
        G_state(:,state) = 0.0_dp

        test_eigenvalue = eigenvalue(state)
        if ( solving_method == 1 ) then
           call Runge_up(test_eigenvalue)
           call Runge_down(test_eigenvalue)
        else if ( solving_method == 2 ) then
           call FGIntegral(test_eigenvalue)
        end if

        ! scale the solutions to make the
        ! match point smooth
        scalefactor = G_state(match+1,state)/G_state(match,state)
        G_state(:match,state) = G_state(:match,state)*scalefactor
        F_state(:match,state) = F_state(:match,state)*scalefactor
        ! calculate integral |F|^2 + |G|^2 (extended Simpson's Rule)
        sum_integral = 0.0_dp
        sum_integral = sum_integral + h_step*(abs(F_state(1,state))**2 + abs(G_state(1,state))**2)
        sum_integral = sum_integral + h_step*(abs(F_state(n_steps,state))**2 + abs(G_state(n_steps,state))**2)
        do r_it = 2, n_steps-2, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 2.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        do r_it = 3, n_steps-1, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 4.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        sum_integral = sum_integral/3.0_dp
        ! normalize
        F_state(:,state) = F_state(:,state)/sqrt(abs(sum_integral))
        G_state(:,state) = G_state(:,state)/sqrt(abs(sum_integral))
        ! calculate discontinuity
        Fdiff = (F_state(match+1,state) - F_state(match,state))/F_state(match,state)

        F_state(:,state) = 0.0_dp
        G_state(:,state) = 0.0_dp

        test_eigenvalue = (1.0_dp+proportional_factor)*eigenvalue(state)
        if ( solving_method == 1 ) then
           call Runge_up(test_eigenvalue)
           call Runge_down(test_eigenvalue)
        else if ( solving_method == 2 ) then
           call FGIntegral(test_eigenvalue)
        end if

        ! scale the solutions to make the 
        ! match point smooth
        scalefactor = G_state(match+1,state)/G_state(match,state)
        G_state(:match,state) = G_state(:match,state)*scalefactor
        F_state(:match,state) = F_state(:match,state)*scalefactor
        ! calculate integral |F|^2 + |G|^2 (extended Simpson's Rule)
        sum_integral = 0.0_dp
        sum_integral = sum_integral + h_step*(abs(F_state(1,state))**2 + abs(G_state(1,state))**2)
        sum_integral = sum_integral + h_step*(abs(F_state(n_steps,state))**2 + abs(G_state(n_steps,state))**2)
        do r_it = 2, n_steps-2, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 2.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        do r_it = 3, n_steps-1, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 4.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        sum_integral = sum_integral/3.0_dp
        ! normalize
        F_state(:,state) = F_state(:,state)/sqrt(abs(sum_integral))
        G_state(:,state) = G_state(:,state)/sqrt(abs(sum_integral))
        ! calculate discontinuity
        Fdiff_up = (F_state(match+1,state) - F_state(match,state))/F_state(match,state)

        F_state(:,state) = 0.0_dp
        G_state(:,state) = 0.0_dp

        test_eigenvalue = (1.0_dp-proportional_factor)*eigenvalue(state)
        if ( solving_method == 1 ) then
           call Runge_up(test_eigenvalue)
           call Runge_down(test_eigenvalue)
        else if ( solving_method == 2 ) then
           call FGIntegral(test_eigenvalue)
        end if

        ! scale the solutions to make the 
        ! match point smooth
        scalefactor = G_state(match+1,state)/G_state(match,state)
        G_state(:match,state) = G_state(:match,state)*scalefactor
        F_state(:match,state) = F_state(:match,state)*scalefactor
        ! calculate integral |F|^2 + |G|^2 (extended Simpson's Rule)
        sum_integral = 0.0_dp
        sum_integral = sum_integral + h_step*(abs(F_state(1,state))**2 + abs(G_state(1,state))**2)
        sum_integral = sum_integral + h_step*(abs(F_state(n_steps,state))**2 + abs(G_state(n_steps,state))**2)
        do r_it = 2, n_steps-2, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 2.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        do r_it = 3, n_steps-1, 2
           !
           radius = r_it*h_step
           sum_integral = sum_integral &
                & + 4.0_dp*h_step*(abs(F_state(r_it,state))**2 + abs(G_state(r_it,state))**2)
           !
        end do
        sum_integral = sum_integral/3.0_dp
        ! normalize
        F_state(:,state) = F_state(:,state)/sqrt(abs(sum_integral))
        G_state(:,state) = G_state(:,state)/sqrt(abs(sum_integral))
        ! calculate discontinuity
        Fdiff_down = (F_state(match+1,state) - F_state(match,state))/F_state(match,state)

        write(*,*)"central = ",Fdiff
        write(*,*)"up      = ",Fdiff_up
        write(*,*)"down    = ",Fdiff_down

        if ( ( abs(Fdiff_down) < abs(Fdiff) ) .and. ( abs(Fdiff_up) < abs(Fdiff) ) ) then
           !
           if ( abs(Fdiff_up) .le. abs(Fdiff_down) ) then
              eigenvalue(state) = (1.0_dp+proportional_factor)*eigenvalue(state)
           end if
           if ( abs(Fdiff_down) .le. abs(Fdiff_up) ) then
              eigenvalue(state) = (1.0_dp-proportional_factor)*eigenvalue(state)
           end if
        else
           if ( abs(Fdiff_up) < abs(Fdiff) ) then
              eigenvalue(state) = (1.0_dp+proportional_factor)*eigenvalue(state)
           end if
           if ( abs(Fdiff_down) < abs(Fdiff) ) then
              eigenvalue(state) = (1.0_dp-proportional_factor)*eigenvalue(state)
           end if
           if ( ( abs(Fdiff_down) > abs(Fdiff) ) .and. ( abs(Fdiff_up) > abs(Fdiff) ) ) then
              ! "Solution is in a minimum"
              proportional_factor = 0.1_dp*proportional_factor
           end if
        end if

        if ( abs(proportional_factor) < yErrReq ) then
           print *,"proportional factor is small enough now... done"
           go to 51
        end if

        if ( guess == 200 ) STOP "can't find EV"
        !
     end do ! guess

51   continue
     !
     write(*,*)"THE EVALUE OF STATE ",state," IS ",eigenvalue(state)*fermi*1000," keV"
     write(*,*)"THE EXACT SOL OF STATE  ",state," IS ",exact_solution(state)*fermi*1000," keV"
     !
     ! write(*,*)"THE EVALUE OF STATE ",state," IS ",eigenvalue(state)," fm^(-1)"
     ! write(*,*)"THE EXACT SOL OF STATE  ",state," IS ",exact_solution(state)," fm^(-1)"
     !
     go to 52

     !! COUNT NODES:
     if ( m_reduced - eigenvalue(state) .gt. 0.0_dp ) then
        nodes(state) = 0
        current_sign = int(G_state(10,state)/abs(G_state(10,state)))
        do r_it = 11, n_steps
           if ( abs(G_state(r_it,state)) > 0.0_dp ) new_sign = int(G_state(r_it,state)/abs(G_state(r_it,state)))
           if ( new_sign /= current_sign ) then 
              nodes(state) = nodes(state) + 1
              current_sign = new_sign
           end if
        end do
     else
        nodes(state) = 99
     end if
     !
     write(*,*)" This state appears to have ",nodes(state)," nodes"
     !!
     if ( ( nodes(state) == expected_nodes(state) ) ) then
        accept_ev = 1
     else
        accept_ev = 0
     end if
     !
     if ( accept_ev == 1 ) then
        write(*,*)"<< CORRECT NUMBER OF NODES! >>"
        go to 52
        !
     else if ( accept_ev == 0 ) then
        ! Incorrect number of nodes - change starting point
        write(*,*)"INCORRECT NUMBER OF NODES!"
        eigenvalue(state) = eigenvalue(state)*(1.05_dp)
     end if
     !
     !
52   continue
     !
     write(*,*)"THE EIGENVALUE OF STATE ",state," IS ",eigenvalue(state)*fermi*1000," keV"
     !
     open(61,file='Wavefunctions.dat',status='unknown')
     do r_it = 1, n_steps, 1000
        write(61,*)r_it*h_step,F_state(r_it,state),G_state(r_it,state)
     end do
     close(61)
     !
  end do ! state

end program FindEigenvalue




subroutine myDerivs(r, params, dydr)

  use shared
  use funcs

  implicit none

  real(dp), intent(in)  :: r, params(3)
  real(dp), intent(out) :: dydr(num_states)
  !
  real(dp) :: F_local, G_local, lambda
  !
  F_local = params(1)
  G_local = params(2)
  lambda  = params(3)
  !
!!$  dydr(1) =  F_local*kappa(state)/r - (lambda - m_reduced + Coulomb(r))*G_local
!!$  dydr(2) = -G_local*kappa(state)/r + (lambda + m_reduced + Coulomb(r))*F_local
  dydr(1) =  F_local*kappa(state)/r - (lambda - Coulomb(r))*G_local
  dydr(2) = -G_local*kappa(state)/r + (lambda + 2.0_dp*m_reduced - Coulomb(r))*F_local
  dydr(3) = 0.0_dp
  !
end subroutine myDerivs


subroutine FGIntegral(input_val)

  use shared
  use funcs

  implicit none

  real(dp), intent(in) :: input_val

  real(dp), dimension(3) :: initial_vals

  real(dp) :: current_radius, V0
  real(dp), dimension(3) :: current_vals, current_derivs, new_vals, calc_error

!!$  real(dp) :: gamma, gamma_func

  integer :: rad_it, term

  real(dp), dimension(3) :: start_vals, end_vals, start_derivs, end_derivs, old_derivs, oldest_derivs
  real(dp) :: temp_derivs(4)

  real(dp) :: Gup, Gdown, Fup, Fdown

  real(dp), dimension(3) :: n0_derivs, n1_derivs, n2_derivs, n3_derivs, n4_derivs

  real(dp) :: coeff(5), deriv_term(5,num_states)

  old_derivs = 0.0_dp
  oldest_derivs = 0.0_dp

  F_state(:,state) = 0.0_dp
  G_state(:,state) = 0.0_dp

  n0_derivs = 0.0_dp
  n1_derivs = 0.0_dp
  n2_derivs = 0.0_dp
  n3_derivs = 0.0_dp

!!$  V0 = (-3.0_dp/2.0_dp)*alpha/test_radius

!!$  print *,"input val = ",input_val

!!$  V0 = Coulomb(2.0_dp*h_step)

  do rad_it = 1, 4
     !
     current_radius = h_step*rad_it
     V0 = Coulomb(current_radius)
     !
!!$     F_state(rad_it,state) = (V0+m_reduced-input_val)*(current_radius**2)/3.0_dp
!!$     G_state(rad_it,state) = -current_radius*(1.0_dp+((current_radius**2)*(input_val+m_reduced-V0)*(V0+m_reduced-input_val)/6.0_dp))

! lambda = E - m
!!$     F_state(rad_it,state) = -(V0-input_val)*(current_radius**2)/3.0_dp
!!$     G_state(rad_it,state) = current_radius*(1.0_dp+((current_radius**2)*(input_val+2.0_dp*m_reduced-V0)*(V0-input_val)/6.0_dp))

!!$  gamma_func = 1.9999_dp
!!$  gamma = sqrt(1.0_dp-(alpha**2))

!!$     F_state(rad_it,state) = -(((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))*(1.0_dp-gamma)/alpha
!!$     !
!!$     G_state(rad_it,state) = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))

!!$  F_state(rad_it,state) = (V0-input_val)*(current_radius**2)/3.0_dp!exact_F(current_radius)
!!$  G_state(rad_it,state) = current_radius*(1.0_dp+((current_radius**2)*(input_val+2.0_dp*m_reduced-V0)*(V0-input_val)/6.0_dp))!exact_G(current_radius)

  F_state(rad_it,state) = exact_F(current_radius)
  G_state(rad_it,state) = exact_G(current_radius)


!!$     F_state(rad_it,state) = current_radius - m_reduced*alpha*(current_radius**2)
!!$     G_state(rad_it,state) = current_radius*alpha/2.0_dp
     !
     current_vals(1) = F_state(rad_it,state)
     current_vals(2) = G_state(rad_it,state)
     current_vals(3) = input_val
     !
     call myDerivs(current_radius,current_vals,temp_derivs(rad_it))     ! EULER
     !
  end do

  n0_derivs = temp_derivs(1)
  n1_derivs = temp_derivs(2)
  n2_derivs = temp_derivs(3)
  n3_derivs = temp_derivs(4)

  current_radius = h_step

  ! 5-step Adams Bashford:
  coeff(5) =  1901.0_dp/720.0_dp
  coeff(4) = -1387.0_dp/360.0_dp
  coeff(3) = 109.0_dp/30.0_dp
  coeff(2) =  -637.0_dp/360.0_dp
  coeff(1) = 251.0_dp/720.0_dp

  do rad_it = 5, match 

     call myDerivs(current_radius+4.0_dp*h_step,current_vals,n4_derivs)
!!$     current_vals = current_vals + h_step*((55.0_dp/24.0_dp)*n3_derivs - (59.0_dp/24.0_dp)*n2_derivs &
!!$          & + (37.0_dp/24.0_dp)*n1_derivs - (3.0_dp/8.0_dp)*n0_derivs)   ! 4sAB

     deriv_term(1,:) = n0_derivs(:)
     deriv_term(2,:) = n1_derivs(:)
     deriv_term(3,:) = n2_derivs(:)
     deriv_term(4,:) = n3_derivs(:)
     deriv_term(5,:) = n4_derivs(:)

     do term = 1, 5
        current_vals(:) = current_vals(:) + h_step*(coeff(term)*deriv_term(term,:))
     end do

     n0_derivs = n1_derivs
     n1_derivs = n2_derivs
     n2_derivs = n3_derivs
     n3_derivs = n4_derivs

     F_state(rad_it,state) = current_vals(1)
     G_state(rad_it,state) = current_vals(2)

     current_radius = current_radius + h_step

  end do

  Gup = G_state(match,state)
  Fup = F_state(match,state)

!!$  gamma_func = 1.9999_dp
!!$  gamma = sqrt(1.0_dp-(alpha**2))

  do rad_it = 1, 4
     !
     current_radius = h_step*(n_steps-rad_it+1)
     !
     !
!!$     F_state(n_steps-rad_it+1,state) = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*&
!!$          & ((2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))*(1.0_dp-gamma)/alpha
!!$     !
!!$     G_state(n_steps-rad_it+1,state) = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*&
!!$          & ((2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))
     !
     !
!     F_state(n_steps-rad_it+1,state) = -(1.0_dp-gamma)/alpha
!!$     F_state(n_steps-rad_it+1,state) = ((2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))*(1.0_dp-gamma)/alpha
     !
!     G_state(n_steps-rad_it+1,state) = 1.0_dp!(2.0_dp*m_reduced*alpha*current_radius)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*current_radius))
     !

     F_state(n_steps-rad_it+1,state) = exact_F(current_radius)
     G_state(n_steps-rad_it+1,state) = exact_G(current_radius)

     current_vals(1) = F_state(n_steps-rad_it+1,state)
     current_vals(2) = G_state(n_steps-rad_it+1,state)
     current_vals(3) = input_val
     !
     call myDerivs(current_radius,current_vals,temp_derivs(rad_it))     ! EULER
     !
  end do

  n0_derivs = temp_derivs(1)
  n1_derivs = temp_derivs(2)
  n2_derivs = temp_derivs(3)
  n3_derivs = temp_derivs(4)

  current_radius = n_steps*h_step

  do rad_it = n_steps-4, match+1, -1

     call myDerivs(current_radius-4.0_dp*h_step,current_vals,n4_derivs)
!!$     current_vals = current_vals + h_step*((55.0_dp/24.0_dp)*n3_derivs - (59.0_dp/24.0_dp)*n2_derivs &
!!$          & + (37.0_dp/24.0_dp)*n1_derivs - (3.0_dp/8.0_dp)*n0_derivs)   ! 4sAB

     deriv_term(1,:) = n0_derivs(:)
     deriv_term(2,:) = n1_derivs(:)
     deriv_term(3,:) = n2_derivs(:)
     deriv_term(4,:) = n3_derivs(:)
     deriv_term(5,:) = n4_derivs(:)

     do term = 1, 5
        current_vals(:) = current_vals(:) - h_step*(coeff(term)*deriv_term(term,:))
     end do

     n0_derivs = n1_derivs
     n1_derivs = n2_derivs
     n2_derivs = n3_derivs
     n3_derivs = n4_derivs

     F_state(rad_it,state) = current_vals(1)
     G_state(rad_it,state) = current_vals(2)

     current_radius = current_radius - h_step

  end do

  Gdown = G_state(match+1,state)
  Fdown = F_state(match+1,state)

  RETURN

end subroutine FGIntegral


subroutine Runge_up(eigen)

  use shared
  use funcs

  implicit none

  real(dp), intent(in) :: eigen

  real(dp) :: tempF(n_steps),  tempG(n_steps), tempL(n_steps)
  real(dp), dimension(3) :: KF1, KF2, KF3, KF4, temp_params, tempdydr

  real(dp) :: temp_rad, newrad
  real(dp) :: newF, newG, newL

  real(dp) :: V0

  integer :: ki

  tempL(1) = eigen

!!$  V0 = Coulomb(2.0_dp*h_step)
!!$  V0 = (-3.0_dp/2.0_dp)*alpha/test_radius

  do ki = 1, 5
     !
     temp_rad = h_step*ki
     V0 = Coulomb(temp_rad)
     !
!     F_state(ki,state) = (V0-eigen)*(temp_rad**2)/3.0_dp

     if ( state == 1 ) F_state(ki,state) = exact_F(temp_rad)
     if ( state == 2 ) F_state(ki,state) = exact_F(temp_rad)

!!$     F_state(ki,state) = (V0+m_reduced-eigen)*(temp_rad)/3.0_dp
     tempF(ki) = F_state(ki,state)


!     G_state(ki,state) = temp_rad*(1.0_dp+((temp_rad**2)*(eigen+2.0_dp*m_reduced-V0)*(V0-eigen)/6.0_dp))

     if ( state == 1 ) G_state(ki,state) = exact_G(temp_rad)
     if ( state == 2 ) G_state(ki,state) = -exact_G(temp_rad)

!!$     G_state(ki,state) = exact_G(temp_rad)
!!$     G_state(ki,state) = -(1.0_dp+((temp_rad**2)*(eigen+m_reduced-V0)*(V0+m_reduced-eigen)/6.0_dp))
     tempG(ki) = G_state(ki,state)
     tempL(ki) = eigen
     !

  end do

  do ki = 5, match-1

     temp_params = (/ tempF(ki), tempG(ki), tempL(ki) /)

     call myDerivs(temp_rad,temp_params,tempdydr)

     KF1 = tempdydr

     newrad = temp_rad + h_step/2.0_dp
     newF = tempF(ki) + h_step*KF1(1)/2.0_dp
     newG = tempG(ki) + h_step*KF1(2)/2.0_dp
     newL = tempL(ki) + h_step*KF1(3)/2.0_dp

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF2 = tempdydr

     newrad = temp_rad + h_step/2.0_dp
     newF = tempF(ki) + h_step*KF2(1)/2.0_dp
     newG = tempG(ki) + h_step*KF2(2)/2.0_dp
     newL = tempL(ki) + h_step*KF2(3)/2.0_dp

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF3 = tempdydr

     newrad = temp_rad + h_step
     newF = tempF(ki) + h_step*KF3(1)
     newG = tempG(ki) + h_step*KF3(2)
     newL = tempL(ki) + h_step*KF3(3)

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF4 = tempdydr

     tempF(ki+1) = tempF(ki) + h_step*(KF1(1)+2.0_dp*KF2(1)+2.0_dp*KF3(1)+KF4(1))/6.0_dp
     tempG(ki+1) = tempG(ki) + h_step*(KF1(2)+2.0_dp*KF2(2)+2.0_dp*KF3(2)+KF4(2))/6.0_dp
     tempL(ki+1) = tempL(ki) + h_step*(KF1(3)+2.0_dp*KF2(3)+2.0_dp*KF3(3)+KF4(3))/6.0_dp

     F_state(ki+1,state) = tempF(ki+1)
     G_state(ki+1,state) = tempG(ki+1)

     temp_rad = temp_rad + h_step

  end do

end subroutine Runge_up


subroutine Runge_down(eigen)

  use shared
  use funcs

  implicit none

  real(dp), intent(in) :: eigen

  real(dp) :: tempF(n_steps),  tempG(n_steps), tempL(n_steps)
  real(dp), dimension(3) :: KF1, KF2, KF3, KF4, temp_params, tempdydr

  real(dp) :: V0!, gamma, gamma_func

  real(dp) :: temp_rad, newrad
  real(dp) :: newF, newG, newL

  integer :: ki

  tempL(n_steps) = eigen

!!$  V0 = (-3.0_dp/2.0_dp)*alpha/test_radius
!!$  gamma_func = 1.9999_dp
!!$  gamma = sqrt(1.0_dp-(alpha**2))

  ! Fill the last 100 points via the r->inf limit
  do ki = n_steps, n_steps-5, -1
     !
     temp_rad = h_step*ki
     !
!!$     F_state(ki,state) = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*temp_rad)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*temp_rad))*(1.0_dp-gamma)/alpha


!!$     if ( state == 1 ) F_state(ki,state) = -(exp(-m_reduced*alpha*temp_rad))*(1.0_dp-gamma)/alpha
!!$     if ( state == 2 ) F_state(ki,state) = (exp(-m_reduced*alpha*temp_rad))*(1.0_dp-gamma)/alpha


     if ( state == 1 ) F_state(ki,state) = exact_F(temp_rad)
     if ( state == 2 ) F_state(ki,state) = -0.0001_dp*exact_F(temp_rad)

     tempF(ki) = F_state(ki,state)

!!$     G_state(ki,state) = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*temp_rad)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*temp_rad))

!!$     G_state(ki,state) = (exp(-m_reduced*alpha*temp_rad))

     if ( state == 1 ) G_state(ki,state) = exact_G(temp_rad)
     if ( state == 2 ) G_state(ki,state) = 0.0_dp*exact_G(temp_rad)


     tempG(ki) = G_state(ki,state)

     tempL(ki) = eigen
     !
  end do

  do ki = n_steps-5, match+2, -1

     temp_params = (/ tempF(ki), tempG(ki), tempL(ki) /)

     call myDerivs(temp_rad,temp_params,tempdydr)

     KF1 = tempdydr

     newrad = temp_rad - h_step/2.0_dp
     newF = tempF(ki) - h_step*KF1(1)/2.0_dp
     newG = tempG(ki) - h_step*KF1(2)/2.0_dp
     newL = tempL(ki) - h_step*KF1(3)/2.0_dp

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF2 = tempdydr

     newrad = temp_rad - h_step/2.0_dp
     newF = tempF(ki) - h_step*KF2(1)/2.0_dp
     newG = tempG(ki) - h_step*KF2(2)/2.0_dp
     newL = tempL(ki) - h_step*KF2(3)/2.0_dp

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF3 = tempdydr

     newrad = temp_rad - h_step
     newF = tempF(ki) - h_step*KF3(1)
     newG = tempG(ki) - h_step*KF3(2)
     newL = tempL(ki) - h_step*KF3(3)

     temp_params = (/ newF, newG, newL /)

     call myDerivs(newrad,temp_params,tempdydr)

     KF4 = tempdydr

     tempF(ki-1) = tempF(ki) - h_step*(KF1(1)+2.0_dp*KF2(1)+2.0_dp*KF3(1)+KF4(1))/6.0_dp
     tempG(ki-1) = tempG(ki) - h_step*(KF1(2)+2.0_dp*KF2(2)+2.0_dp*KF3(2)+KF4(2))/6.0_dp
     tempL(ki-1) = tempL(ki) - h_step*(KF1(3)+2.0_dp*KF2(3)+2.0_dp*KF3(3)+KF4(3))/6.0_dp

     F_state(ki-1,state) = tempF(ki-1)
     G_state(ki-1,state) = tempG(ki-1)

     temp_rad = temp_rad - h_step

  end do

end subroutine Runge_down
