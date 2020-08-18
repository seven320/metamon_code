-- +goose Up
    INSERT into user (
        username,
        user_id,
        twitter_id,
        secret_account
    )
    values
    ('電電','123456','yosyuaomenww',0),
    ('しげ', '7','seven320', 1);
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
DELETE FROM user WHERE user_id = '123456';
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
