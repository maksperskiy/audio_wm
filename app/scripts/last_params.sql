select distinct on (label, experiment_number) zfirst_value(step_number) OVER (
        partition by label,
        experiment_number
        order by created_at desc
    ) as step_number,
    label,
    experiment_number,
    first_value(freq_bottom) OVER (
        partition by label,
        experiment_number
        order by created_at desc
    ) as freq_bottom,
    first_value(freq_top) OVER (
        partition by label,
        experiment_number
        order by created_at desc
    ) as freq_top,
    first_value(duration) OVER (
        partition by label,
        experiment_number
        order by created_at desc
    ) as duration
from params_history
where param_number is null;


select distinct on (label, experiment_number) first_value(step_number) OVER (
        partition by label
        order by created_at desc,
            experiment_number desc
    ) as step_number,
    label,
    first_value(experiment_number) OVER (
        partition by label
        order by created_at desc,
            experiment_number desc
    ) as experiment_number,
    first_value(freq_bottom) OVER (
        partition by label
        order by created_at desc,
            experiment_number desc
    ) as freq_bottom,
    first_value(freq_top) OVER (
        partition by label
        order by created_at desc,
            experiment_number desc
    ) as freq_top,
    first_value(duration) OVER (
        partition by label
        order by created_at desc,
            experiment_number desc
    ) as duration
from params_history
where param_number is null;