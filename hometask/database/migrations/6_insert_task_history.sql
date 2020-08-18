-- +goose Up
    INSERT into task_history(
        task_id,
        tweet_id,
        tweet_text,
        praised
    )
    value
    (
        '1',
        '1295657389354409985',
        '#hometask 今日も新機能開発',
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
