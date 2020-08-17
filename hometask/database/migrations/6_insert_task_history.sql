-- +goose Up
    INSERT into task_history(
        task_id,
        praised
    )
    value
    (
        '1',
        0
    );
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
    DELETE FROM task_history WHERE task_id = '1';
-- -- +goose StatementBegin
-- SELECT 'down SQL query';
-- -- +goose StatementEnd
