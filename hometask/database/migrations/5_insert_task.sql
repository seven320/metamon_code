-- +goose Up
    INSERT into task (
        user_id,
        task
    )
    values
    ('123456', '朝早く起きる'),
    ('123456', '早寝早起き'),
    ('123456', '本を読む'),
    ('7', '英単語を勉強する'),
    ('7', '長文を読む');
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
DELETE FROM task WHERE user_id = '123456';
-- +goose StatementBegin
-- SELECT 'down SQL query';
-- +goose StatementEnd
