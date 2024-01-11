function initialize(box)
    dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")
    dofile(box:get_config("${Player_ScenarioDirectory}") .. "/scripts/stimuli.lua")

    local num_trials = 40
    local num_blocks = 3
    local durations = {
        ISI = { 0.300, 0.400, 0.500 },           --s
        ITI = { 0.800, 0.900, 1.000, 1.100, 1.200 }, --s, these are the set of possible ITIs
    }

    -- Create the list of blocks
    ITI = {}
    ISI = {}
    blocks = {}
    for _ = 1, num_blocks do
        -- Create the list of trials
        trials = {}
        local odd_count = 0
        for k = 1, num_trials do
            random_num = math.random(0, 10)

            if random_num > 2.5 then
                table.insert(trials, stimcodes.shapes.freq)
            else
                table.insert(trials, stimcodes.shapes.non_freq)
                odd_count  = odd_count + 1
            end
            table.insert(ITI, durations.ITI[k % #durations.ITI +1])
            table.insert(ISI, durations.ISI[k % #durations.ISI +1])
        end
        box:log('Warning',tostring(odd_count))
        table.insert(blocks, trials)
    end

     -- shuffle the ITIs
    ITI = shuffle_arr(ITI)
     -- shuffle the ISIs
    ISI = shuffle_arr(ISI)

end

-- function show_instructions(box, stim, t)
--     box:send_stimulation(1, stim, t, 0)
--     t = wait_for_continue(box)
-- end

-- this function is called once by the box
function process(box)
    local t = box:get_current_time()

    -- Start the experiment
    box:send_stimulation(1, stimcodes.experiment_start, t, 0)

    -- Display the first set of instructions
    for k, stim in ipairs(stimcodes.instructions.set_0) do
        box:send_stimulation(1, stim, t, 0)
        t = wait_for_continue(box)
    end

    -- Display the second set of instructions
    for k, stim in ipairs(stimcodes.instructions.set_1) do
        box:send_stimulation(1, stim, t, 0)
        t = wait_for_continue(box)
    end

    -- box:log('Warning',tostring(#blocks))


    for b_t, trials in ipairs(blocks) do
        box:send_stimulation(1, stimcodes.instructions.set_1.blk_strt, t, 0)
        t = wait_for_continue(box)

        -- Iterate through trials
        t = t + 0.2
        for k_t, trial in pairs(trials) do
            -- Assume that at start of loop, `t` is the time of the start of
            -- the trial


            interval_index =  (b_t - 1) * (#trials) + k_t

            -- box:log('Warning', tostring(interval_index))

            -- Indicate start of trial
            box:send_stimulation(1, stimcodes.trial_start, t, 0)

            -- Show fixation cross
            box:send_stimulation(1, stimcodes.fixation_cross, t, 0)
            t = t + ISI[interval_index]
            -- box:send_stimulation(1, stimcodes.clear_screen, t, 0)

            -- Show the stimulus
            box:send_stimulation(1, trial, t, 0)
            t = t + ITI[interval_index]
            -- box:send_stimulation(1, stimcodes.clear_screen, t, 0)

            -- End the trial and wait for the next trial
            box:send_stimulation(1, stimcodes.trial_stop, t, 0)
            box:send_stimulation(1, stimcodes.clear_screen, t, 0)
            t = t + 0.05
        end

        box:send_stimulation(1, stimcodes.instructions.set_1.blk_end, t, 0)
        t = wait_for_continue(box)
    end

    -- end the experiment
    box:send_stimulation(1,  stimcodes.instructions.set_2.exp_end, t, 0)
    t = t + 1

    box:send_stimulation(1, stimcodes.experiment_stop, t, 0)
end

function wait_for_continue(box)
    -- loop until box:keep_processing() returns zero
    -- cpu will be released with a call to sleep
    -- at the end of the loop
    while box:keep_processing() do
        -- specify the stimulation that implies to stop waiting
        local target_stimulation = OVTK_StimulationId_Number_1B

        -- loop through all inputs of the box
        for input = 1, box:get_input_count() do
            -- loop through every received stimulation for the input
            for stimulation = 1, box:get_stimulation_count(input) do
                -- get the received stimulation and discard it
                local identifier, _, _ = box:get_stimulation(input, 1)
                box:remove_stimulation(input, 1)

                -- return the time if the target stimulation is was received
                if identifier == target_stimulation then
                    return box:get_current_time()
                end
            end
        end

        -- release cpu
        box:sleep()
    end
end

function shuffle_arr(arr)
    local s = {}

    -- copy original array
    for k, _ in ipairs(arr) do
        s[k] = arr[k]
    end

    -- shuffle the copied array
    for i = #arr, 2, -1 do
        local j = math.random(i)
        s[i], s[j] = s[j], s[i]
    end

    return s
end

function wait_for(box, duration)
    local t0 = box:get_current_time()

    -- loop until box:keep_processing() returns zero
    -- cpu will be released with a call to sleep
    -- at the end of the loop
    while box:keep_processing() do
        -- Get the current time
        local t = box:get_current_time()

        -- Return the time after waiting for the specified duration
        if t - t0 >= duration then
            return t
        end

        -- release cpu
        box:sleep()
    end
end

function wait_until(box, time)
    while box:get_current_time() < time do
        box:sleep()
    end
end
