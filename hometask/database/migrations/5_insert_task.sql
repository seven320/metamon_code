-- +goose Up
    INSERT into task (
        user_id,
        task
    )
    values
    (
        '123456',
        '朝早く起きる'
    );
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
DELETE FROM task WHERE user_id == '123456'
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
