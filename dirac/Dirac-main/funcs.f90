module funcs

  implicit none

contains

  function Coulomb(rad)

    use shared  
!    use myIntegrate

    implicit none

    real(dp), intent(in) :: rad
    real(dp) :: Coulomb

    !! finite charge distribution - requires integration
!!$    Coulomb = -alpha*((4.0_dp*pi_d/rad)*integral(c_func1,0.0_dp,rad,abs_err,rel_err) &
!!$         & + (4.0_dp*pi_d)*integral(c_func2,rad,huge(1.0_dp),abs_err,rel_err))
!!$

    !! point charge distribution
    Coulomb = -alpha/rad

  end function Coulomb

!!$  function Coulomb_2(rad)
!!$
!!$    use shared
!!$    use myIntegrate
!!$
!!$    implicit none
!!$
!!$    real(dp), intent(in) :: rad
!!$    real(dp) :: Coulomb_2
!!$
!!$    Coulomb_2 = -alpha*((4.0_dp*pi_d)*integral(c_func2,rad,huge(1.0_dp),abs_err,rel_err))
!!$
!!$  end function Coulomb_2

  function c_func1(rad)

    use shared

    implicit none

    real(dp), intent(in) :: rad
    real(dp) :: c_func1

    c_func1 = (rad**2)*rho(rad)

  end function c_func1

  function c_func2(rad)

    use shared

    implicit none

    real(dp), intent(in) :: rad
    real(dp) :: c_func2

    c_func2 = rad*rho(rad)  !! r^2 * rho / r

  end function c_func2

  function rho(rad)

    use shared
!    use myIntegrate

    implicit none

    real(dp), intent(in) :: rad
    real(dp) :: rho
    real(dp) :: c1, c2

!!$    c1 = (4.0_dp*pi_d*integral(c_func3,0.0_dp,huge(1.0_dp),abs_err,rel_err))**(-1)
    c2 = sqrt(12.0_dp/(test_radius**2))
    c1 = (c2**3)/(8.0_dp*pi_d)

    rho = c1*exp(-c2*rad)

  end function rho

!!$  function c_func3(rad)
!!$
!!$    use shared  
!!$
!!$    implicit none
!!$
!!$    real(dp), intent(in) :: rad
!!$    real(dp) :: c_func3
!!$    real(dp) :: c2
!!$
!!$    c2 = sqrt(12.0_dp/(test_radius**2))
!!$
!!$    c_func3 = (rad**2)*exp(-c2*rad)
!!$
!!$  end function c_func3


  function exact_F(r)

    use shared
!    use myIntegrate

    implicit none

    real(dp), intent(in) :: r
    real(dp) :: exact_F

!!$    real(dp) :: gamma, gamma_func

!!$     gamma = sqrt(1.0_dp-(alpha**2))

!!$     gamma_func = 1.9999_dp
!!$     gamma_func = 2.0_dp*gamma*integral(gfunc,0.0_dp,huge(1.0_dp),abs_err,rel_err)

    exact_F = (((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*r)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*r))*(1.0_dp-gamma)/alpha

  end function exact_F

!!$  function gfunc(t)
!!$
!!$    use shared
!!$
!!$    implicit none
!!$
!!$    real(dp), intent(in) :: t
!!$    real(dp) :: gfunc, gamma
!!$
!!$    gamma = sqrt(1.0_dp-(alpha**2))
!!$
!!$    gfunc = t**(2.0_dp*gamma - 1.0_dp)*(exp(-t))
!!$
!!$  end function gfunc

  function exact_G(r)

    use shared

    implicit none

    real(dp), intent(in) :: r
    real(dp) :: exact_G

!!$    real(dp) :: gamma, gamma_func
!!$
!!$     gamma_func = 1.9999_dp
!!$     gamma = sqrt(1.0_dp-(alpha**2))

     exact_G = -(((2.0_dp*m_reduced*alpha)**(3.0_dp/2.0_dp))/(sqrt(4.0_dp*pi_d)))*(sqrt((1+gamma)/(2.0_dp*euler_gamma_func)))*((2.0_dp*m_reduced*alpha*r)**(gamma-1.0_dp))*(exp(-m_reduced*alpha*r))

  end function exact_G

end module funcs
