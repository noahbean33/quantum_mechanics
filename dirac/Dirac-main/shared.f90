module shared

  use nrtype

  implicit none

  !! (CODATA)
  real(dp), parameter :: fermi = 197.3269631_dp            ! hbar*c (MeV fm)  or kev 1000fm
  real(dp), parameter :: m_proton = 938.272013_dp/fermi    ! m_p (fm) or .001fm
  real(dp), parameter :: m_electron = 0.510998910_dp/fermi ! m_e (fm) or .001fm
  !!  real(dp), parameter :: m_muon     = 105.6583668_dp/fermi ! m_mu !!JDC2023 use electron
  real(dp), parameter :: m_muon = m_electron

  real(dp), parameter :: m_reduced = (m_muon*m_proton)/(m_muon+m_proton)
  !!$  real(dp), parameter :: m_reduced = m_muon
  real(dp), parameter :: test_radius = 0.84184_dp
  real(dp), parameter :: physical_radius = 0.84184_dp

  real(dp), parameter :: alpha = 0.0072973525376_dp ! fine structure constant

  real(dp), parameter :: gamma = 0.999973373968498_dp           ! gamma = SQRT[1-alpha**2]
  real(dp), parameter :: euler_gamma_func = 1.99990172319612_dp ! GAMMA[1+2gamma] calculated fully

  integer(I8B), parameter :: n_steps = 500*1e5_I8B ! number of steps (5000 fm)
  integer(I8B), parameter :: match   = 100*1e3_I8B  ! match point number (680 fm) or 282
  !integer(I8B), parameter :: n_steps = 4000e4_I8B ! number of steps (2000 fm)
  ! integer(I8B), parameter :: match   = 500e4_I8B  ! match point number == 1s(1/2)
  !!$integer(I8B), parameter :: match   = 282e4_I8B  ! match point number == 2s(1/2)

  integer, parameter :: max_attempts = 1e4  ! max number of attempts to solve

  real(dp), parameter :: h_step  = 1.0e-2_dp  ! step size = 1/100 fm
 !! real(dp), parameter :: yErrReq = 1.0e-12_dp      ! required precision (!) !!JDC2023
  real(dp), parameter :: yErrReq = 1.0e-6_dp      ! required precision (!) 

  real(dp), parameter :: abs_err = 1.0e-10_dp
  real(dp), parameter :: rel_err = 0.0_dp

  integer, parameter :: num_states = 3

  integer, dimension(num_states), parameter :: expected_nodes = (/ 0, 1, 0 /)

  integer, dimension(num_states), parameter :: kappa = (/ -1, -1, 1 /)

  !! Globals: !!

  integer(I8B)  :: state
!  real(dp) :: F_state(n_steps,num_states), G_state(n_steps,num_states), PSI_F(n_steps), PSI_G(n_steps)
  real(dp), dimension(:,:), allocatable :: F_state, G_state!, PSI_F, PSI_G


end module shared
