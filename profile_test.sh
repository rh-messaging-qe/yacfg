#!/usr/bin/env bash

# prepare test independent temporary path
PID=$$
tmp_dir="/tmp/yacfg_profile_test-${PID}"

list_profiles=()
list_ecode_generate=()
list_ecode_export=()
list_ecode_export_static=()
list_ecode_export_tuning=()
list_ecode_tune=()
list_yamllint_static=()
list_yamllint_tuning=()


PROCESS_LIMIT=$(nproc)
PROCESS_LIMIT=${PROCESS_LIMIT:=8}

if (( $# > 0 )); then
  profiles="$*"
else
  profiles="$(yacfg --list-profiles)"
fi


function process_barrier {
  while (( $(jobs | wc -l) >= PROCESS_LIMIT )); do
    sleep 0.1
  done
}

i=0
  # generator check
pid_list=()

for p in ${profiles}; do
    echo ">> $p"
done

for p in ${profiles}; do
    (( i++ ))
    list_profiles+=( "$p" )

    yacfg --profile "$p" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_ecode_generate+=( $? )
done


  # dynamic profile

pid_list=()
for p in ${profiles}; do
    yacfg --profile "$p" --new-profile "$tmp_dir/profile/dynamic/$p" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_ecode_export+=( $? )
done

  # static profile

pid_list=()
for p in ${profiles}; do
    static_profile_path="$tmp_dir/profile/static/$p.yaml"

    yacfg --profile "$p" --new-profile-static "$static_profile_path" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_ecode_export_static+=( $? )
done

  # profile tuning

pid_list=()
for p in ${profiles}; do
    tuning_path="$tmp_dir/profile/tuning/$p.yaml"

    yacfg --profile "$p" --export-tuning "$tuning_path" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_ecode_export_tuning+=( $? )
done


  ## Phase2

# YAML Lint static profile

pid_list=()
for p in ${profiles}; do
    static_profile_path="$tmp_dir/profile/static/$p.yaml"
    yamllint "${static_profile_path}" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_yamllint_static+=( $? )
done

# YAML Lint tuning

pid_list=()
for p in ${profiles}; do
    tuning_path="$tmp_dir/profile/tuning/$p.yaml"
    yamllint "${tuning_path}" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_yamllint_tuning+=( $? )
done

# Tune profile

pid_list=()
for p in ${profiles}; do
    yacfg --profile "$p" --tune "$tuning_path" &
    pid_list+=( $! )
    process_barrier
done

for pid in "${pid_list[@]}"; do
    wait "${pid}"
    list_ecode_tune+=( $? )
done

    # stop

    #if (( i > 11 )); then
    #    break
    #fi

#done

echo "--- Results:"
echo "Generation    : ${list_ecode_generate[*]}"
echo "Export dynamic: ${list_ecode_export[*]}"
echo "Export static : ${list_ecode_export_static[*]}"
echo "Y-lint static : ${list_yamllint_static[*]}"
echo "Export tuning : ${list_ecode_export_tuning[*]}"
echo "Y-lint tuning : ${list_yamllint_tuning[*]}"
echo "Tune Profile  : ${list_ecode_tune[*]}"

# echo "Profiles: ${list_profiles[@]}"

total_ecode=0

for (( i=0; i < ${#list_profiles[@]}; i++ )); do
    ecode_gen=${list_ecode_generate[i]}
    ecode_exp=${list_ecode_export[i]}
    ecode_exps=${list_ecode_export_static[i]}
    ecode_ystat=${list_yamllint_static[i]}
    ecode_tun=${list_ecode_export_tuning[i]}
    ecode_ytun=${list_yamllint_tuning[i]}
    ecode_tune=${list_ecode_tune[i]}

    ecode_vector="${ecode_gen}${ecode_exp}${ecode_exps}${ecode_ystat}${ecode_tun}${ecode_ytun}${ecode_tune}"

    if [[ ! $ecode_vector =~ ^0+$ ]]; then
        echo "${list_profiles[i]}: g:${ecode_gen}, d:${ecode_exp}, s:${ecode_exps}, ${ecode_ystat}, t:${ecode_tun}, ${ecode_ytun}, ${ecode_tune}"
        total_ecode=1
    fi
done

rm -fr "${tmp_dir}"

exit $total_ecode
