# Dodanie punktu zamykającego krzywą (domykający okrąg)
x_points_closed = x_points + [x_points[0]]
y_points_closed = y_points + [y_points[0]]
t_uniform = np.linspace(0, 1, len(x_points_closed))

# Interpolacja sklejanymi wielomianami dla równomiernych punktów t
cs_x_uniform = CubicSpline(t_uniform, x_points_closed, bc_type='periodic')
cs_y_uniform = CubicSpline(t_uniform, y_points_closed, bc_type='periodic')

# Wyznaczenie współczynników
coefficients_x_uniform = cs_x_uniform.c.T
coefficients_y_uniform = cs_y_uniform.c.T

# Przypisanie wyników do czytelnych tabel
interval_labels_uniform = [f'Interval {i}-{i+1}' for i in range(len(t_uniform) - 1)]
coeff_table_x_uniform = pd.DataFrame(coefficients_x_uniform, columns=['a', 'b', 'c', 'd'], index=interval_labels_uniform)
coeff_table_y_uniform = pd.DataFrame(coefficients_y_uniform, columns=['a', 'b', 'c', 'd'], index=interval_labels_uniform)

import ace_tools as tools; tools.display_dataframe_to_user(name="Spline Coefficients for x(t) with Uniform t", dataframe=coeff_table_x_uniform)
tools.display_dataframe_to_user(name="Spline Coefficients for y(t) with Uniform t", dataframe=coeff_table_y_uniform)
