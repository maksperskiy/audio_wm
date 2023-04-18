select distinct on (label) first_value(step_number) OVER (
        partition by label
        order by created_at desc
    ) as step_number,
    label,
    first_value(freq_bottom) OVER (
        partition by label
        order by created_at desc
    ) as freq_bottom,
    first_value(freq_top) OVER (
        partition by label
        order by created_at desc
    ) as freq_top,
    first_value(duration) OVER (
        partition by label
        order by created_at desc
    ) as duration
from params_history
where param_number is null;