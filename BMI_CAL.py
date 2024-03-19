import streamlit as st

def calculate_roots(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root, root
    else:
        real_part = -b / (2*a)
        imaginary_part = (-discriminant)**0.5 / (2*a)
        return complex(real_part, imaginary_part), complex(real_part, -imaginary_part)

def main():
    st.title("Quadratic Equation Solver")
    st.write("Enter the coefficients of the quadratic equation ax^2 + bx + c = 0")

    a = st.number_input("Enter a:", value=1.0)
    b = st.number_input("Enter b:", value=0.0)
    c = st.number_input("Enter c:", value=0.0)

    if st.button("Calculate Roots"):
        root1, root2 = calculate_roots(a, b, c)
        st.success(f"Root 1: {root1}")
        st.success(f"Root 2: {root2}")

if _name_ == "_main_":
    main()
