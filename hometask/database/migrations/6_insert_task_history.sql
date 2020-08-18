-- +goose Up
    INSERT into task_history(
        task_id,
        tweet_id,
        tweet_text,
        praised
    )
    values
    ('1', '12956573', '#hometask 8時に起きた',0),
    ('1', '7654323456', '7時に起きた',0),
    ('3', '7654323456722', 'アガサクリスティ読んだ', 1),
    ('4', '654321234567', 'p10 ~ p12', 0),
    ('4', '235432', 'p13 ~ p15', 0),
    ('4', '234567654', 'p16~p20', 0),
    ('5', '32435423', '長文3p読んだ',0);
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
    DELETE FROM task_history WHERE task_id = '1';
-- -- +goose StatementBegin
-- SELECT 'down SQL query';
-- -- +goose StatementEnd
